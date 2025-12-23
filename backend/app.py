from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError, InvalidHeaderError, NoAuthorizationError
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, UnprocessableEntity
from datetime import datetime, timedelta, date, timezone
from sqlalchemy import func, text
from models import db, User, Product, Team, TeamMember, Content, Commission, Payment, ManagerBonus, DailyCommission, VideoStatistic, MemberDailySummary, Notification
from utils import validate_product_data, validate_user_data, sanitize_string, validate_url
import os
import logging
import re
import json
import requests
from dotenv import load_dotenv

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../frontend')
# Validate required environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# In production, fail fast if secrets not set
if os.getenv('FLASK_ENV') == 'production':
    if not SECRET_KEY or SECRET_KEY == 'your-secret-key-change-this':
        raise ValueError("SECRET_KEY must be set in production environment")
    if not JWT_SECRET_KEY or JWT_SECRET_KEY == 'jwt-secret-key-change-this':
        raise ValueError("JWT_SECRET_KEY must be set in production environment")

# Use fallback only for development
app.config['SECRET_KEY'] = SECRET_KEY or 'your-secret-key-change-this-dev-only'
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY or 'jwt-secret-key-change-this-dev-only'

if not SECRET_KEY or not JWT_SECRET_KEY:
    logger.warning("⚠️  Using default secrets. Change SECRET_KEY and JWT_SECRET_KEY in production!")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'  # Use 'error' instead of 'msg' for consistency
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///affiliate_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Database connection pooling (for SQLite, will help when migrating to PostgreSQL)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {'check_same_thread': False}  # SQLite specific
}

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# JWT Error Handlers - prevent 422 errors from JWT validation
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token telah kadaluarsa. Silakan login lagi.'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    logger.warning(f"Invalid JWT token: {error}")
    return jsonify({'error': 'Token tidak valid. Silakan login lagi.'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    logger.warning(f"Missing JWT token: {error}")
    return jsonify({'error': 'Token tidak ditemukan. Silakan login.'}), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token perlu di-refresh. Silakan login lagi.'}), 401

# Helper function untuk get user_id dari JWT token
def get_current_user_id():
    """Get current user ID from JWT token (converts string to int)"""
    user_id_str = get_jwt_identity()
    if not user_id_str:
        return None
    try:
        return int(user_id_str)
    except (ValueError, TypeError):
        return None

# Response compression
try:
    from flask_compress import Compress
    Compress(app)
    logger.info("Response compression enabled")
except ImportError:
    logger.warning("flask-compress not installed, compression disabled")

# Rate limiting
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"  # Use memory for development, Redis for production
    )
    logger.info("Rate limiting enabled")
except ImportError:
    logger.warning("flask-limiter not installed, rate limiting disabled")
    limiter = None

# Request logging middleware
@app.before_request
def log_request_info():
    """Log all incoming requests"""
    logger.info(f"{request.method} {request.path} - IP: {request.remote_addr}")
    logger.debug(f"Query params: {dict(request.args)}")
    logger.debug(f"Headers: Authorization={request.headers.get('Authorization', 'None')[:50]}")
    # Only log JSON body for POST/PUT/PATCH requests that actually have content
    if request.method in ['POST', 'PUT', 'PATCH'] and request.is_json and request.content_length:
        if request.path not in ['/api/auth/login', '/api/auth/register']:
            try:
                body = request.get_json(silent=True)
                if body:
                    logger.debug(f"Request body: {body}")
            except Exception:
                pass  # Skip logging if JSON parsing fails

@app.after_request
def log_response_info(response):
    """Log response status"""
    logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
    return response

# ==================== HEALTH CHECK ====================
@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
        logger.error(f"Database health check failed: {e}")
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'database': db_status,
        'version': '1.0'
    }), 200 if db_status == 'healthy' else 503

# Global error handler untuk memastikan semua error return JSON
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found: {request.method} {request.path}")
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Server Error: {str(error)}", exc_info=True)
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    """Handle 400 Bad Request errors"""
    logger.warning(f"400 Bad Request: {e}")
    logger.warning(f"Request path: {request.path}, Method: {request.method}")
    logger.warning(f"Query params: {dict(request.args)}")
    return jsonify({'error': 'Invalid request. Pastikan semua parameter valid.'}), 400

@app.errorhandler(UnprocessableEntity)
@app.errorhandler(422)
def handle_422_error(e):
    """Handle 422 Unprocessable Entity errors from Flask/Werkzeug"""
    import traceback
    logger.error(f"422 Error: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    logger.error(f"Request path: {request.path}, Method: {request.method}")
    logger.error(f"Query params: {dict(request.args)}")
    logger.error(f"Request headers: {dict(request.headers)}")
    logger.error(f"Full traceback: {traceback.format_exc()}")
    if request.is_json:
        logger.error(f"Request JSON: {request.get_json(silent=True)}")
    else:
        logger.error(f"Request data: {request.get_data(as_text=True)[:500]}")
    
    # Check if error is from JWT
    error_str = str(e).lower()
    if 'jwt' in error_str or 'token' in error_str or 'authorization' in error_str:
        return jsonify({'error': 'Token tidak valid. Silakan login lagi.', 'details': str(e)}), 401
    
    # Provide more specific error message based on request type
    if request.method == 'GET':
        error_msg = 'Invalid query parameters. Pastikan parameter page dan per_page adalah angka yang valid.'
    else:
        error_msg = 'Data tidak valid. Pastikan semua field diisi dengan benar dan format data sesuai.'
    
    return jsonify({'error': error_msg, 'details': str(e)}), 422

@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler - hide internal errors in production"""
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    import traceback
    
    # In development, show detailed error
    if app.config.get('DEBUG') or os.getenv('FLASK_ENV') == 'development':
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }), 500
    else:
        # In production, hide internal errors
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please contact support.'
        }), 500

# Initialize database
with app.app_context():
    # Only drop tables in development mode
    # In production, use Flask-Migrate for proper migrations
    if os.getenv('FLASK_ENV') == 'development' or os.getenv('DEBUG') == 'True':
        try:
            db.drop_all()
            print("🗑️  Old database schema dropped (development mode)")
        except Exception as e:
            logger.warning(f"Could not drop tables: {e}")
    
    # Create all tables with new schema
    try:
        db.create_all()
        print("✅ Database schema created/verified")
    except Exception as e:
        logger.error(f"Error creating database schema: {e}")
        raise
    
    # Auto-migrate: Add missing columns if needed (for existing databases)
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'products' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('products')]
            # Add sheet_order column if missing
            if 'sheet_order' not in columns:
                logger.info("🔄 Adding sheet_order column to products table (auto-migration)...")
                db.session.execute(text("ALTER TABLE products ADD COLUMN sheet_order INTEGER"))
                db.session.commit()
                logger.info("✅ sheet_order column added successfully")
            # Add item_terjual column if missing
            if 'item_terjual' not in columns:
                logger.info("🔄 Adding item_terjual column to products table (auto-migration)...")
                db.session.execute(text("ALTER TABLE products ADD COLUMN item_terjual INTEGER DEFAULT 0"))
                db.session.commit()
                logger.info("✅ item_terjual column added successfully")
    except Exception as e:
        # Column might already exist or table doesn't exist yet
        if 'duplicate column' not in str(e).lower() and 'no such table' not in str(e).lower():
            logger.warning(f"Could not add columns (might already exist): {e}")
    
    # Create default owner if not exists
    if not User.query.filter_by(role='owner').first():
        owner = User(
            username='owner',
            email='owner@affiliate.com',
            password_hash=generate_password_hash('admin123'),
            role='owner',
            full_name='Owner'
        )
        db.session.add(owner)
        db.session.commit()

# ==================== AUTH ====================
@app.route('/api/auth/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON or empty request body'}), 400
    
    # Input validation
    if not data.get('username'):
        return jsonify({'error': 'Username is required'}), 400
    if not data.get('password'):
        return jsonify({'error': 'Password is required'}), 400
    
    # Sanitize input
    username = sanitize_string(data.get('username', ''), max_length=80)
    if not username:
        return jsonify({'error': 'Invalid username'}), 400
    
    # Validate user data
    is_valid, error_msg = validate_user_data(data)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username sudah ada'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'member'),
        full_name=data.get('full_name', '')
    )
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'full_name': user.full_name
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON or empty request body'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'full_name': user.full_name
            }
        }), 200
    
    return jsonify({'error': 'Username atau password salah'}), 401

# ==================== USERS ====================
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users with pagination and search"""
    # Get user_id from token (already validated by @jwt_required)
    # Pagination - safe parsing to avoid 422 errors
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1
    
    try:
        per_page = int(request.args.get('per_page', 20))
        if per_page < 1:
            per_page = 20
        per_page = min(per_page, 100)  # Max 100 per page
    except (ValueError, TypeError):
        per_page = 20
    
    # Search
    search = request.args.get('search', '').strip()
    
    # Build query
    query = User.query
    
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            db.or_(
                User.full_name.like(search_filter),
                User.username.like(search_filter),
                User.email.like(search_filter),
                User.telegram_username.like(search_filter)
            )
        )
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items
    
    return jsonify({
        'users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email or '',
            'role': u.role,
            'full_name': u.full_name or '',
            'whatsapp': u.whatsapp or '',
            'tiktok_akun': u.tiktok_akun or '',
            'wallet': u.wallet or '',
            'bank_account': u.bank_account or '',
            'telegram_username': u.telegram_username or '',
            'created_at': u.created_at.strftime('%Y-%m-%d') if u.created_at else ''
        } for u in users],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user (owner only)"""
    current_user_id = get_current_user_id()
    if not current_user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    current_user = db.session.get(User, current_user_id)
    if not current_user or current_user.role != 'owner':
        return jsonify({'error': 'Only owner can update users'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.json
    
    # Update fields
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'email' in data:
        user.email = data['email']
    if 'whatsapp' in data:
        user.whatsapp = data['whatsapp']
    if 'wallet' in data:
        user.wallet = data['wallet']
    if 'bank_account' in data:
        user.bank_account = data['bank_account']
    if 'role' in data and current_user.role == 'owner':
        user.role = data['role']
    
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email or '',
        'role': user.role,
        'full_name': user.full_name or '',
        'whatsapp': user.whatsapp or '',
        'wallet': user.wallet or '',
        'bank_account': user.bank_account or ''
    }), 200

# ==================== MY PROFILE (User-specific) ====================
@app.route('/api/my/profile', methods=['GET'])
@jwt_required()
def get_my_profile():
    """Get current user's profile"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'whatsapp': user.whatsapp or '',
        'tiktok_akun': user.tiktok_akun or '',
        'wallet': user.wallet or '',
        'bank_account': user.bank_account or '',
        'telegram_username': user.telegram_username or '',
        'role': user.role,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }), 200

@app.route('/api/my/profile', methods=['PUT'])
@jwt_required()
def update_my_profile():
    """Update current user's own profile"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = User.query.get_or_404(user_id)
    data = request.json
    
    # User can only update their own profile fields (not role)
    if 'full_name' in data:
        user.full_name = data['full_name'].strip()
    if 'email' in data:
        user.email = data['email'].strip()
    if 'whatsapp' in data:
        user.whatsapp = data['whatsapp'].strip()
    if 'wallet' in data:
        user.wallet = data['wallet'].strip()
    if 'bank_account' in data:
        user.bank_account = data['bank_account'].strip()
    
    db.session.commit()
    
    # Update Google Sheets
    try:
        gs_service = GoogleSheetsService()
        if gs_service.is_available():
            gs_service.update_user_in_sheet(user)
    except Exception as e:
        print(f"Warning: Failed to update user in Google Sheets: {e}")
    
    return jsonify({
        'message': 'Profile berhasil diupdate',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'whatsapp': user.whatsapp or '',
            'wallet': user.wallet or '',
            'bank_account': user.bank_account or ''
        }
    }), 200

# ==================== PRODUCTS ====================
@app.route('/api/products/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get TikTok product categories"""
    try:
        categories = [
            'Fashion & Apparel',
            'Beauty & Personal Care',
            'Electronics',
            'Home & Living',
            'Food & Beverage',
            'Health & Wellness',
            'Sports & Outdoors',
            'Toys & Games',
            'Books & Media',
            'Automotive',
            'Pet Supplies',
            'Baby & Kids',
            'Jewelry & Accessories',
            'Office Supplies',
            'Travel & Luggage',
            'Musical Instruments',
            'Art & Crafts',
            'Garden & Tools',
            'Phone & Accessories',
            'Computer & Accessories',
            'Camera & Photo',
            'Smart Home',
            'Fitness & Exercise',
            'Outdoor Recreation',
            'Party Supplies',
            'Stationery',
            'Kitchen & Dining',
            'Bath & Body',
            'Hair Care',
            'Skincare',
            'Makeup',
            'Fragrance',
            'Men\'s Fashion',
            'Women\'s Fashion',
            'Kids\' Fashion',
            'Shoes',
            'Bags & Wallets',
            'Watches',
            'Sunglasses',
            'Other'
        ]
        return jsonify(categories), 200
    except Exception as e:
        print(f"Error in get_categories: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
@jwt_required(optional=False)
def get_products():
    """Get all products with pagination, filtering, and search"""
    try:
        # Pagination - safe parsing to avoid 422 errors
        try:
            page = int(request.args.get('page', 1))
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1
        
        try:
            per_page = int(request.args.get('per_page', 20))
            if per_page < 1:
                per_page = 20
            per_page = min(per_page, 100)  # Max 100 per page
        except (ValueError, TypeError):
            per_page = 20
        
        # Filters
        status_filter = request.args.get('status', '').strip()
        category_filter = request.args.get('category', '').strip()
        search = request.args.get('search', '').strip()
        
        # Build query
        query = Product.query
        
        # Apply filters
        if status_filter:
            query = query.filter(Product.status == status_filter)
        
        if category_filter:
            query = query.filter(Product.category == category_filter)
        
        if search:
            search_filter = f'%{search}%'
            query = query.filter(
                db.or_(
                    Product.product_name.like(search_filter),
                    Product.category.like(search_filter)
                )
            )
        
        # Order by sheet_order (Google Sheets row order), then by ID as fallback
        # Use COALESCE to handle NULL sheet_order values
        try:
            from sqlalchemy import func
            query = query.order_by(
                func.coalesce(Product.sheet_order, Product.id).asc(),
                Product.id.asc()
            )
        except Exception as e:
            logger.error(f"Error ordering products: {e}")
            # Fallback to ID if sheet_order not available
            query = query.order_by(Product.id.asc())
        
        # Paginate
        try:
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            products = pagination.items
        except Exception as e:
            logger.error(f"Error paginating products: {e}", exc_info=True)
            return jsonify({'error': f'Error loading products: {str(e)}'}), 500
        
        return jsonify({
            'products': [{
                'id': p.id,
                'product_name': p.product_name,
                'category': p.category,
                'product_link': p.product_link,
                'product_price': float(p.product_price) if p.product_price else 0,
                'commission_percent': float(p.commission_percent) if p.commission_percent else 0,
                'regular_commission': float(p.regular_commission) if p.regular_commission else 0,
                'gmv_max_commission': float(p.gmv_max_commission) if p.gmv_max_commission else 0,
                'target_gmv': float(p.target_gmv) if p.target_gmv else 0,
                'item_terjual': int(getattr(p, 'item_terjual', 0) or 0),
                'status': p.status,
                'created_at': p.created_at.isoformat() if p.created_at else None
            } for p in products],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
    except Exception as e:
        logger.error(f"Unexpected error in get_products: {e}", exc_info=True)
        return jsonify({'error': f'Error loading products: {str(e)}'}), 500

@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    """Create new product"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa menambah produk'}), 403
    
    # Validate JSON
    if not request.is_json:
        logger.warning(f"Create product: Content-Type not JSON. Content-Type: {request.content_type}")
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    data = request.get_json(silent=True)
    if not data:
        logger.warning(f"Create product: Invalid JSON or empty body. Raw data: {request.get_data(as_text=True)[:200]}")
        return jsonify({'error': 'Invalid JSON or empty request body'}), 400
    
    logger.info(f"Create product request data: {data}")
    
    # Validate required fields
    required_fields = ['product_name', 'category', 'product_link', 'product_price']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif isinstance(data[field], str) and not data[field].strip():
            missing_fields.append(field)
        elif data[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        logger.warning(f"Create product: Missing required fields: {missing_fields}")
        return jsonify({'error': f'Field berikut harus diisi: {", ".join(missing_fields)}'}), 400
    
    # Validate numeric fields - handle odd numbers and decimals
    try:
        # Convert to string first to handle any formatting, then to float
        price_str = str(data['product_price']).strip().replace(',', '')
        product_price = float(price_str)
        if product_price <= 0:
            logger.warning(f"Create product: Invalid product_price: {data['product_price']}")
            return jsonify({'error': 'Harga produk harus lebih dari 0'}), 400
        # Round to 2 decimal places for consistency
        product_price = round(product_price, 2)
    except (ValueError, TypeError) as e:
        logger.warning(f"Create product: product_price conversion error: {e}, value: {data.get('product_price')}")
        return jsonify({'error': f'Harga produk harus berupa angka. Diterima: {data.get("product_price")}'}), 400
    
    # Calculate commissions from percentage if provided - handle odd numbers
    try:
        # Helper function to safely convert to float
        def safe_float(value, default=0):
            if value is None or value == '':
                return default
            if isinstance(value, str):
                value = value.strip().replace(',', '')
            try:
                return float(value) if value else default
            except (ValueError, TypeError):
                return default
        
        commission_percent = safe_float(data.get('commission_percent', 0))
        gmv_percent = safe_float(data.get('gmv_percent', 0))
        regular_commission = safe_float(data.get('regular_commission', 0))
        gmv_max_commission = safe_float(data.get('gmv_max_commission', 0))
    except (ValueError, TypeError) as e:
        logger.warning(f"Create product: Commission conversion error: {e}, data: {data.get('commission_percent')}, {data.get('gmv_percent')}")
        return jsonify({'error': 'Komisi harus berupa angka yang valid'}), 400
    
    # Priority: Use percentages if provided, otherwise use direct values
    # If commission_percent provided, calculate from percentage
    if commission_percent > 0:
        regular_commission = (product_price * commission_percent) / 100
        logger.info(f"Calculated regular_commission from {commission_percent}%: {regular_commission}")
    elif regular_commission <= 0:
        logger.warning(f"Create product: No commission_percent or regular_commission provided")
        return jsonify({'error': 'Komisi reguler harus diisi (persentase atau nominal)'}), 400
    
    # If gmv_percent provided, calculate from percentage
    if gmv_percent > 0:
        gmv_max_commission = (product_price * gmv_percent) / 100
        logger.info(f"Calculated gmv_max_commission from {gmv_percent}%: {gmv_max_commission}")
    elif gmv_max_commission <= 0:
        logger.warning(f"Create product: No gmv_percent or gmv_max_commission provided")
        return jsonify({'error': 'Komisi GMV harus diisi (persentase atau nominal)'}), 400
    
    # Recalculate commission_percent if not provided but regular_commission is
    if commission_percent == 0 and regular_commission > 0:
        commission_percent = (regular_commission / product_price) * 100
    
    # Validate target_gmv - handle odd numbers
    try:
        target_gmv_str = str(data.get('target_gmv', 0) or 0).strip().replace(',', '')
        target_gmv = float(target_gmv_str) if target_gmv_str else 0
        target_gmv = round(target_gmv, 2)
    except (ValueError, TypeError):
        target_gmv = 0
    
    # Validate item_terjual - handle odd numbers
    try:
        item_terjual_str = str(data.get('item_terjual', 0) or 0).strip().replace(',', '')
        item_terjual = int(float(item_terjual_str)) if item_terjual_str else 0
        if item_terjual < 0:
            item_terjual = 0
    except (ValueError, TypeError):
        item_terjual = 0
    
    try:
        product = Product(
            product_name=data['product_name'].strip(),
            category=data.get('category', 'General').strip(),
            product_link=data['product_link'].strip(),
            product_price=product_price,
            commission_percent=round(commission_percent, 2),
            regular_commission=round(regular_commission, 2),
            gmv_max_commission=round(gmv_max_commission, 2),
            target_gmv=target_gmv,
            item_terjual=item_terjual,
            status=data.get('status', 'active')
        )
        logger.info(f"Creating product: {product.product_name}")
    except Exception as e:
        logger.error(f"Error creating Product object: {e}", exc_info=True)
        return jsonify({'error': f'Error membuat produk: {str(e)}'}), 500
    try:
        db.session.add(product)
        db.session.commit()
        logger.info(f"Product created successfully: ID={product.id}, Name={product.product_name}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error saving product to database: {e}", exc_info=True)
        return jsonify({'error': f'Error menyimpan produk ke database: {str(e)}'}), 500
    
    # Add to Google Sheets
    try:
        gs_service = GoogleSheetsService()
        if gs_service.is_available():
            gs_service.add_product_to_sheet(product)
            logger.info(f"Product added to Google Sheets: {product.product_name}")
    except Exception as e:
        logger.warning(f"Failed to add product to Google Sheets: {e}")
        # Don't fail the request if Google Sheets fails
    
    # Post to channel (async)
    try:
        channel_service = ChannelService(
            bot_token=os.getenv('TELEGRAM_TOKEN', ''),
            channel_id=os.getenv('CHANNEL_CHAT_ID', '-1003607323066')
        )
        if channel_service.bot:
            # Run async in thread
            def post_to_channel():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(channel_service.post_product_update(product, 'new'))
                loop.close()
            threading.Thread(target=post_to_channel, daemon=True).start()
    except Exception as e:
        print(f"Warning: Failed to post to channel: {e}")
    
    return jsonify({
        'message': 'Produk berhasil ditambahkan',
        'id': product.id,
        'product': {
            'id': product.id,
            'product_name': product.product_name,
            'category': product.category,
            'product_link': product.product_link,
            'product_price': product.product_price,
            'commission_percent': product.commission_percent,
            'regular_commission': product.regular_commission,
            'gmv_max_commission': product.gmv_max_commission
        }
    }), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa mengubah produk'}), 403
    
    product = Product.query.get_or_404(product_id)
    data = request.json
    
    # Update fields
    if 'product_name' in data:
        product.product_name = data['product_name']
    if 'category' in data:
        product.category = data['category']
    if 'product_link' in data:
        product.product_link = data['product_link']
    if 'product_price' in data:
        product.product_price = float(data['product_price'])
    if 'commission_percent' in data:
        product.commission_percent = float(data['commission_percent'])
    if 'regular_commission' in data:
        product.regular_commission = float(data['regular_commission'])
    if 'gmv_max_commission' in data:
        product.gmv_max_commission = float(data['gmv_max_commission'])
    if 'target_gmv' in data:
        try:
            target_gmv_str = str(data['target_gmv'] or 0).strip().replace(',', '')
            product.target_gmv = float(target_gmv_str) if target_gmv_str else 0
        except (ValueError, TypeError):
            product.target_gmv = 0
    if 'item_terjual' in data:
        try:
            item_terjual_str = str(data['item_terjual'] or 0).strip().replace(',', '')
            product.item_terjual = int(float(item_terjual_str)) if item_terjual_str else 0
            if product.item_terjual < 0:
                product.item_terjual = 0
        except (ValueError, TypeError):
            product.item_terjual = 0
    if 'status' in data:
        product.status = data['status']
    
    # Recalculate commission if price or percent changed
    if 'product_price' in data or 'commission_percent' in data:
        if not data.get('regular_commission'):
            product.regular_commission = (product.product_price * product.commission_percent) / 100
    
    db.session.commit()
    return jsonify({'message': 'Produk berhasil diupdate'}), 200

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa menghapus produk'}), 403
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Produk berhasil dihapus'}), 200

# ==================== TEAMS ====================
@app.route('/api/teams', methods=['GET'])
@jwt_required()
def get_teams():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    
    if user.role == 'owner':
        teams = Team.query.all()
    elif user.role == 'manager':
        teams = Team.query.filter_by(manager_id=user_id).all()
    else:
        member = TeamMember.query.filter_by(user_id=user_id).first()
        if member:
            teams = [db.session.get(Team,member.team_id)]
        else:
            teams = []
    
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'manager_id': t.manager_id,
        'manager_name': t.manager.full_name if t.manager else None,
        'target_commission': t.target_commission,
        'manager_bonus_percent': t.manager_bonus_percent,
        'created_at': t.created_at.isoformat()
    } for t in teams]), 200

@app.route('/api/teams', methods=['POST'])
@jwt_required()
def create_team():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa membuat tim'}), 403
    
    data = request.json
    team = Team(
        name=data['name'],
        manager_id=data.get('manager_id'),
        target_commission=data.get('target_commission', 0),
        manager_bonus_percent=data.get('manager_bonus_percent', 5)
    )
    db.session.add(team)
    db.session.commit()
    
    return jsonify({'message': 'Tim berhasil dibuat', 'id': team.id}), 201

@app.route('/api/teams/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team(team_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    
    team = Team.query.get_or_404(team_id)
    
    # Check access
    if user.role != 'owner':
        if user.role == 'manager' and team.manager_id != user_id:
            return jsonify({'error': 'Akses ditolak'}), 403
        elif user.role == 'member':
            member = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
            if not member:
                return jsonify({'error': 'Akses ditolak'}), 403
    
    # Get team members
    members = TeamMember.query.filter_by(team_id=team_id).all()
    member_list = [{
        'id': m.id,
        'user_id': m.user_id,
        'username': m.user.username if m.user else None,
        'full_name': m.user.full_name if m.user else None,
        'joined_at': m.joined_at.isoformat()
    } for m in members]
    
    return jsonify({
        'id': team.id,
        'name': team.name,
        'manager_id': team.manager_id,
        'manager_name': team.manager.full_name if team.manager else None,
        'target_commission': team.target_commission,
        'manager_bonus_percent': team.manager_bonus_percent,
        'members': member_list,
        'created_at': team.created_at.isoformat()
    }), 200

@app.route('/api/teams/<int:team_id>', methods=['PUT'])
@jwt_required()
def update_team(team_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa mengubah tim'}), 403
    
    team = Team.query.get_or_404(team_id)
    data = request.json
    
    if 'name' in data:
        team.name = data['name']
    if 'manager_id' in data:
        team.manager_id = data.get('manager_id') if data.get('manager_id') else None
    if 'target_commission' in data:
        team.target_commission = float(data['target_commission'])
    if 'manager_bonus_percent' in data:
        team.manager_bonus_percent = float(data['manager_bonus_percent'])
    
    db.session.commit()
    return jsonify({'message': 'Tim berhasil diupdate'}), 200

@app.route('/api/teams/<int:team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa menghapus tim'}), 403
    
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    
    return jsonify({'message': 'Tim berhasil dihapus'}), 200

@app.route('/api/teams/<int:team_id>/members', methods=['GET'])
@jwt_required()
def get_team_members(team_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    
    team = Team.query.get_or_404(team_id)
    
    # Check access
    if user.role != 'owner':
        if user.role == 'manager' and team.manager_id != user_id:
            return jsonify({'error': 'Akses ditolak'}), 403
        elif user.role == 'member':
            member = TeamMember.query.filter_by(team_id=team_id, user_id=user_id).first()
            if not member:
                return jsonify({'error': 'Akses ditolak'}), 403
    
    members = TeamMember.query.filter_by(team_id=team_id).all()
    return jsonify([{
        'id': m.id,
        'user_id': m.user_id,
        'username': m.user.username if m.user else None,
        'full_name': m.user.full_name if m.user else None,
        'email': m.user.email if m.user else None,
        'joined_at': m.joined_at.isoformat()
    } for m in members]), 200

@app.route('/api/teams/<int:team_id>/members', methods=['POST'])
@jwt_required()
def add_team_member(team_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa menambah member'}), 403
    
    data = request.json
    if 'user_id' not in data:
        return jsonify({'error': 'user_id harus diisi'}), 400
    
    # Check if member already in team
    existing = TeamMember.query.filter_by(team_id=team_id, user_id=data['user_id']).first()
    if existing:
        return jsonify({'error': 'Member sudah ada di tim ini'}), 400
    
    member = TeamMember(
        team_id=team_id,
        user_id=data['user_id']
    )
    db.session.add(member)
    db.session.commit()
    
    return jsonify({'message': 'Member berhasil ditambahkan', 'id': member.id}), 201

@app.route('/api/teams/<int:team_id>/members/<int:member_id>', methods=['DELETE'])
@jwt_required()
def remove_team_member(team_id, member_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa menghapus member'}), 403
    
    member = TeamMember.query.filter_by(id=member_id, team_id=team_id).first_or_404()
    db.session.delete(member)
    db.session.commit()
    
    return jsonify({'message': 'Member berhasil dihapus dari tim'}), 200

# ==================== CONTENT ====================
@app.route('/api/content', methods=['GET'])
@jwt_required()
def get_content():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    
    if user.role == 'owner':
        contents = Content.query.all()
    elif user.role == 'manager':
        team = Team.query.filter_by(manager_id=user_id).first()
        if team:
            member_ids = [m.user_id for m in TeamMember.query.filter_by(team_id=team.id).all()]
            contents = Content.query.filter(Content.creator_id.in_(member_ids)).all()
        else:
            contents = []
    else:
        contents = Content.query.filter_by(creator_id=user_id).all()
    
    return jsonify([{
        'id': c.id,
        'product_id': c.product_id,
        'product_title': c.product.product_name if c.product else None,
        'creator_id': c.creator_id,
        'creator_name': c.creator.full_name if c.creator else None,
        'title': c.title,
        'description': c.description,
        'media_url': c.media_url,
        'link_video': c.link_video or '',
        'tanggal_upload': c.tanggal_upload.strftime('%d/%m/%Y') if c.tanggal_upload else '',
        'tiktok_akun': c.tiktok_akun or '',
        'platform': c.platform,
        'quality_score': c.quality_score,
        'status': c.status,
        'created_at': c.created_at.isoformat()
    } for c in contents]), 200

@app.route('/api/content', methods=['POST'])
@jwt_required()
def create_content():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    data = request.json
    
    content = Content(
        product_id=data['product_id'],
        creator_id=user_id,
        title=data['title'],
        description=data.get('description', ''),
        media_url=data.get('media_url', ''),
        platform=data.get('platform', 'tiktok'),
        quality_score=data.get('quality_score', 0),
        status='pending'
    )
    db.session.add(content)
    db.session.commit()
    
    return jsonify({'message': 'Konten berhasil dibuat', 'id': content.id}), 201

@app.route('/api/content/<int:content_id>/approve', methods=['POST'])
@jwt_required()
def approve_content(content_id):
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa approve konten'}), 403
    
    content = Content.query.get_or_404(content_id)
    data = request.json
    content.status = 'approved'
    content.quality_score = data.get('quality_score', content.quality_score)
    
    db.session.commit()
    return jsonify({'message': 'Konten berhasil diapprove'}), 200

# ==================== REPORTS (Content dengan link_video) ====================
@app.route('/api/reports', methods=['GET'])
@jwt_required()
def get_reports():
    """Get all reports with pagination, filtering, and search"""
    # Pagination - safe parsing to avoid 422 errors
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1
    
    try:
        per_page = int(request.args.get('per_page', 20))
        if per_page < 1:
            per_page = 20
        per_page = min(per_page, 100)  # Max 100 per page
    except (ValueError, TypeError):
        per_page = 20
    
    # Filters
    status_filter = request.args.get('status', '').strip()
    try:
        user_id_filter = int(request.args.get('user_id')) if request.args.get('user_id') else None
    except (ValueError, TypeError):
        user_id_filter = None
    search = request.args.get('search', '').strip()
    
    # Date filters
    date_from_str = request.args.get('date_from', '').strip()
    date_to_str = request.args.get('date_to', '').strip()
    
    date_from = None
    date_to = None
    
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        except ValueError:
            logger.warning(f"Invalid date_from format: {date_from_str}")
    
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            logger.warning(f"Invalid date_to format: {date_to_str}")
    
    # Build query
    query = Content.query.filter(
        Content.link_video != None,
        Content.link_video != ''
    )
    
    # Apply filters
    if status_filter:
        query = query.filter(Content.status == status_filter)
    
    if user_id_filter:
        query = query.filter(Content.creator_id == user_id_filter)
    
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            db.or_(
                Content.link_video.like(search_filter),
                Content.tiktok_akun.like(search_filter)
            )
        )
    
    # Apply date filters
    if date_from:
        query = query.filter(Content.created_at >= datetime.combine(date_from, datetime.min.time()).replace(tzinfo=timezone.utc))
    if date_to:
        query = query.filter(Content.created_at <= datetime.combine(date_to, datetime.max.time()).replace(tzinfo=timezone.utc))
    
    # Order by created_at desc
    query = query.order_by(Content.created_at.desc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    reports = pagination.items
    
    return jsonify({
        'reports': [{
            'id': r.id,
            'creator_id': r.creator_id,
            'creator_name': r.creator.full_name if r.creator else 'N/A',
            'user_name': r.creator.full_name if r.creator else 'N/A',  # Alias for frontend compatibility
            'link_video': r.link_video,
            'tanggal_upload': r.tanggal_upload.strftime('%Y-%m-%d') if r.tanggal_upload else '',
            'tiktok_akun': r.tiktok_akun or '',
            'status': r.status or 'pending',  # Ensure status is never None
            'quality_score': r.quality_score,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
        } for r in reports],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@app.route('/api/reports/<int:report_id>/approve', methods=['POST'])
@jwt_required()
def approve_report(report_id):
    """Approve a report"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa approve report'}), 403
    
    content = Content.query.get_or_404(report_id)
    if not content.link_video:
        return jsonify({'error': 'Ini bukan report'}), 400
    
    data = request.json or {}
    content.status = 'approved'
    if 'quality_score' in data:
        content.quality_score = float(data['quality_score'])
    
    # Update Google Sheets if available
    try:
        from google_sheets_service import GoogleSheetsService
        gs_service = GoogleSheetsService()
        if gs_service.is_available():
            # Update status in Google Sheets (find by link_video)
            headers = ['nama_user', 'link_video', 'tanggal_upload', 'tiktok_akun', 'status', 'created_at']
            sheet = gs_service.ensure_sheet_exists('laporan', headers)
            if not sheet:
                logger.warning("Sheet 'laporan' tidak bisa diakses untuk update status")
            else:
                all_values = sheet.get_all_values()
                if len(all_values) > 1:
                    sheet_headers = all_values[0]
                    # Find status column index
                    status_col_idx = None
                    for i, h in enumerate(sheet_headers):
                        if h.lower().strip() == 'status':
                            status_col_idx = i + 1  # gspread uses 1-based indexing
                            break
                    
                    if status_col_idx:
                        # Find row by link_video (column index 2, 1-based = 3)
                        link_col_idx = None
                        for i, h in enumerate(sheet_headers):
                            if h.lower().strip() in ['link_video', 'link video']:
                                link_col_idx = i + 1
                                break
                        
                        if link_col_idx:
                            for idx, row in enumerate(all_values[1:], start=2):
                                if len(row) >= link_col_idx and row[link_col_idx - 1] == content.link_video:
                                    sheet.update_cell(idx, status_col_idx, 'approved')
                                    logger.info(f"Updated report status to 'approved' in Google Sheets")
                                    break
    except Exception as e:
        logger.warning(f"Failed to update Google Sheets: {e}")
    
    db.session.commit()
    return jsonify({'message': 'Report berhasil diapprove'}), 200

# ==================== MY REPORTS (User Reports) ====================
@app.route('/api/my/reports', methods=['GET'])
@jwt_required()
def get_my_reports():
    """Get all reports from current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Pagination
        try:
            page = int(request.args.get('page', 1))
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1
        
        try:
            per_page = int(request.args.get('per_page', 20))
            if per_page < 1:
                per_page = 20
            per_page = min(per_page, 100)
        except (ValueError, TypeError):
            per_page = 20
        
        # Filters
        status_filter = request.args.get('status', '').strip()
        search = request.args.get('search', '').strip()
        
        # Date filters
        date_from_str = request.args.get('date_from', '').strip()
        date_to_str = request.args.get('date_to', '').strip()
        
        date_from = None
        date_to = None
        
        if date_from_str:
            try:
                date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"Invalid date_from format: {date_from_str}")
        
        if date_to_str:
            try:
                date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"Invalid date_to format: {date_to_str}")
        
        # Build query - only current user's reports
        query = Content.query.filter(Content.creator_id == current_user_id)
        
        # Apply filters
        if status_filter:
            query = query.filter(Content.status == status_filter)
        
        if search:
            search_filter = f'%{search}%'
            query = query.filter(
                db.or_(
                    Content.link_video.like(search_filter),
                    Content.tiktok_akun.like(search_filter),
                    Content.title.like(search_filter)
                )
            )
        
        # Apply date filters
        if date_from:
            query = query.filter(Content.created_at >= datetime.combine(date_from, datetime.min.time()).replace(tzinfo=timezone.utc))
        if date_to:
            query = query.filter(Content.created_at <= datetime.combine(date_to, datetime.max.time()).replace(tzinfo=timezone.utc))
        
        # Order by created_at desc
        query = query.order_by(Content.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        reports = pagination.items
        
        return jsonify({
            'reports': [{
                'id': r.id,
                'product_id': r.product_id,
                'product_name': r.product.product_name if r.product else None,
                'title': r.title,
                'description': r.description,
                'link_video': r.link_video,
                'tanggal_upload': r.tanggal_upload.strftime('%Y-%m-%d') if r.tanggal_upload else None,
                'tiktok_akun': r.tiktok_akun or '',
                'platform': r.platform or 'tiktok',
                'status': r.status or 'pending',
                'quality_score': r.quality_score or 0,
                'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else '',
                'updated_at': r.updated_at.strftime('%Y-%m-%d %H:%M:%S') if r.updated_at else ''
            } for r in reports],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting my reports: {e}", exc_info=True)
        return jsonify({'error': f'Error loading reports: {str(e)}'}), 500

@app.route('/api/my/reports', methods=['POST'])
@jwt_required()
def create_my_report():
    """Create new report from current user"""
    try:
        current_user_id = get_jwt_identity()
        data = request.json
        
        # Validation
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        link_video = data.get('link_video', '').strip()
        tanggal_upload_str = data.get('tanggal_upload', '').strip()
        tiktok_akun = data.get('tiktok_akun', '').strip()
        product_id = data.get('product_id')
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        platform = data.get('platform', 'tiktok').strip().lower()
        
        # Required fields
        if not link_video:
            return jsonify({'error': 'Link video harus diisi'}), 400
        
        if not tanggal_upload_str:
            return jsonify({'error': 'Tanggal upload harus diisi'}), 400
        
        if not tiktok_akun:
            return jsonify({'error': 'Akun TikTok harus diisi'}), 400
        
        # Parse tanggal
        try:
            tanggal_upload = datetime.strptime(tanggal_upload_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Format tanggal tidak valid. Gunakan format YYYY-MM-DD'}), 400
        
        # Validate product_id if provided
        if product_id:
            try:
                product_id = int(product_id)
                product = Product.query.get(product_id)
                if not product:
                    return jsonify({'error': 'Produk tidak ditemukan'}), 404
            except (ValueError, TypeError):
                return jsonify({'error': 'Product ID tidak valid'}), 400
        
        # Validate platform
        if platform not in ['tiktok', 'shopee']:
            platform = 'tiktok'
        
        # Generate title if not provided
        if not title:
            title = f"Video {platform.capitalize()} - {tiktok_akun}"
        
        # Create content/report
        content = Content(
            creator_id=current_user_id,
            product_id=product_id,
            title=title,
            description=description,
            link_video=link_video,
            tanggal_upload=tanggal_upload,
            tiktok_akun=tiktok_akun,
            platform=platform,
            status='pending'
        )
        
        db.session.add(content)
        db.session.commit()
        
        # Add to Google Sheets
        try:
            from google_sheets_service import GoogleSheetsService
            gs_service = GoogleSheetsService()
            if gs_service.is_available():
                gs_service.add_report_to_sheet(content)
        except Exception as e:
            logger.warning(f"Failed to add report to Google Sheets: {e}")
        
        return jsonify({
            'message': 'Laporan berhasil dibuat',
            'id': content.id,
            'report': {
                'id': content.id,
                'link_video': content.link_video,
                'tanggal_upload': content.tanggal_upload.strftime('%Y-%m-%d') if content.tanggal_upload else None,
                'tiktok_akun': content.tiktok_akun,
                'status': content.status
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating report: {e}", exc_info=True)
        return jsonify({'error': f'Error creating report: {str(e)}'}), 500

@app.route('/api/my/reports/<int:report_id>', methods=['GET'])
@jwt_required()
def get_my_report(report_id):
    """Get single report by ID (only if owned by current user)"""
    try:
        current_user_id = get_jwt_identity()
        
        report = Content.query.filter_by(id=report_id, creator_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Laporan tidak ditemukan'}), 404
        
        return jsonify({
            'id': report.id,
            'product_id': report.product_id,
            'product_name': report.product.product_name if report.product else None,
            'title': report.title,
            'description': report.description,
            'link_video': report.link_video,
            'tanggal_upload': report.tanggal_upload.strftime('%Y-%m-%d') if report.tanggal_upload else None,
            'tiktok_akun': report.tiktok_akun or '',
            'platform': report.platform or 'tiktok',
            'status': report.status or 'pending',
            'quality_score': report.quality_score or 0,
            'created_at': report.created_at.strftime('%Y-%m-%d %H:%M:%S') if report.created_at else '',
            'updated_at': report.updated_at.strftime('%Y-%m-%d %H:%M:%S') if report.updated_at else ''
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting report: {e}", exc_info=True)
        return jsonify({'error': f'Error loading report: {str(e)}'}), 500

@app.route('/api/my/reports/<int:report_id>', methods=['PUT'])
@jwt_required()
def update_my_report(report_id):
    """Update report (only if pending and owned by current user)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.json
        
        report = Content.query.filter_by(id=report_id, creator_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Laporan tidak ditemukan'}), 404
        
        # Only allow edit if status is pending
        if report.status != 'pending':
            return jsonify({'error': 'Hanya laporan dengan status pending yang bisa di-edit'}), 400
        
        # Update fields
        if 'link_video' in data:
            link_video = data.get('link_video', '').strip()
            if link_video:
                report.link_video = link_video
        
        if 'tanggal_upload' in data:
            tanggal_upload_str = data.get('tanggal_upload', '').strip()
            if tanggal_upload_str:
                try:
                    report.tanggal_upload = datetime.strptime(tanggal_upload_str, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Format tanggal tidak valid. Gunakan format YYYY-MM-DD'}), 400
        
        if 'tiktok_akun' in data:
            tiktok_akun = data.get('tiktok_akun', '').strip()
            if tiktok_akun:
                report.tiktok_akun = tiktok_akun
        
        if 'product_id' in data:
            product_id = data.get('product_id')
            if product_id:
                try:
                    product_id = int(product_id)
                    product = Product.query.get(product_id)
                    if not product:
                        return jsonify({'error': 'Produk tidak ditemukan'}), 404
                    report.product_id = product_id
                except (ValueError, TypeError):
                    return jsonify({'error': 'Product ID tidak valid'}), 400
            else:
                report.product_id = None
        
        if 'title' in data:
            title = data.get('title', '').strip()
            if title:
                report.title = title
        
        if 'description' in data:
            report.description = data.get('description', '').strip()
        
        if 'platform' in data:
            platform = data.get('platform', 'tiktok').strip().lower()
            if platform in ['tiktok', 'shopee']:
                report.platform = platform
        
        from datetime import datetime, timezone
        report.updated_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        # Update Google Sheets
        try:
            from google_sheets_service import GoogleSheetsService
            gs_service = GoogleSheetsService()
            if gs_service.is_available():
                gs_service.add_report_to_sheet(report)
        except Exception as e:
            logger.warning(f"Failed to update report in Google Sheets: {e}")
        
        return jsonify({
            'message': 'Laporan berhasil di-update',
            'report': {
                'id': report.id,
                'link_video': report.link_video,
                'tanggal_upload': report.tanggal_upload.strftime('%Y-%m-%d') if report.tanggal_upload else None,
                'tiktok_akun': report.tiktok_akun,
                'status': report.status
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating report: {e}", exc_info=True)
        return jsonify({'error': f'Error updating report: {str(e)}'}), 500

@app.route('/api/my/reports/<int:report_id>', methods=['DELETE'])
@jwt_required()
def delete_my_report(report_id):
    """Delete report (only if pending and owned by current user)"""
    try:
        current_user_id = get_jwt_identity()
        
        report = Content.query.filter_by(id=report_id, creator_id=current_user_id).first()
        
        if not report:
            return jsonify({'error': 'Laporan tidak ditemukan'}), 404
        
        # Only allow delete if status is pending
        if report.status != 'pending':
            return jsonify({'error': 'Hanya laporan dengan status pending yang bisa di-hapus'}), 400
        
        db.session.delete(report)
        db.session.commit()
        
        return jsonify({'message': 'Laporan berhasil di-hapus'}), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting report: {e}", exc_info=True)
        return jsonify({'error': f'Error deleting report: {str(e)}'}), 500

# ==================== NOTIFICATIONS API ====================
@app.route('/api/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get notifications for current user"""
    try:
        current_user_id = get_current_user_id()
        if not current_user_id:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Pagination
        try:
            page = int(request.args.get('page', 1))
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1
        
        try:
            per_page = int(request.args.get('per_page', 20))
            if per_page < 1:
                per_page = 20
            per_page = min(per_page, 100)
        except (ValueError, TypeError):
            per_page = 20
        
        # Filter
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        # Get notifications
        from services.notification_service import NotificationService
        notifications, pagination = NotificationService.get_user_notifications(
            user_id=current_user_id,
            page=page,
            per_page=per_page,
            unread_only=unread_only
        )
        
        # Get unread count
        unread_count = NotificationService.get_unread_count(current_user_id)
        
        return jsonify({
            'notifications': notifications,
            'unread_count': unread_count,
            'pagination': pagination
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting notifications: {e}", exc_info=True)
        return jsonify({'error': f'Error loading notifications: {str(e)}'}), 500

@app.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark notification as read"""
    try:
        current_user_id = get_current_user_id()
        if not current_user_id:
            return jsonify({'error': 'Invalid token'}), 401
        
        from services.notification_service import NotificationService
        success = NotificationService.mark_as_read(notification_id, current_user_id)
        
        if not success:
            return jsonify({'error': 'Notification not found or unauthorized'}), 404
        
        return jsonify({'message': 'Notification marked as read'}), 200
        
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}", exc_info=True)
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/notifications/read-all', methods=['POST'])
@jwt_required()
def mark_all_notifications_read():
    """Mark all notifications as read for current user"""
    try:
        current_user_id = get_current_user_id()
        if not current_user_id:
            return jsonify({'error': 'Invalid token'}), 401
        
        from services.notification_service import NotificationService
        count = NotificationService.mark_all_as_read(current_user_id)
        
        return jsonify({
            'message': f'{count} notifications marked as read',
            'count': count
        }), 200
        
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {e}", exc_info=True)
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/notifications/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete notification"""
    try:
        current_user_id = get_current_user_id()
        if not current_user_id:
            return jsonify({'error': 'Invalid token'}), 401
        
        from services.notification_service import NotificationService
        success = NotificationService.delete_notification(notification_id, current_user_id)
        
        if not success:
            return jsonify({'error': 'Notification not found or unauthorized'}), 404
        
        return jsonify({'message': 'Notification deleted'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting notification: {e}", exc_info=True)
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/notifications/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get unread notification count"""
    try:
        current_user_id = get_current_user_id()
        if not current_user_id:
            return jsonify({'error': 'Invalid token'}), 401
        
        from services.notification_service import NotificationService
        count = NotificationService.get_unread_count(current_user_id)
        
        return jsonify({'unread_count': count}), 200
        
    except Exception as e:
        logger.error(f"Error getting unread count: {e}", exc_info=True)
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/reports/<int:report_id>/reject', methods=['POST'])
@jwt_required()
def reject_report(report_id):
    """Reject a report"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa reject report'}), 403
    
    content = Content.query.get_or_404(report_id)
    if not content.link_video:
        return jsonify({'error': 'Ini bukan report'}), 400
    
    data = request.json or {}
    content.status = 'rejected'
    rejection_notes = data.get('notes', '')
    if rejection_notes:
        content.description = f"Rejected: {rejection_notes}"
    
    # Create notification untuk user
    try:
        from services.notification_service import NotificationService
        NotificationService.create_notification(
            user_id=content.creator_id,
            type='report_rejected',
            title='❌ Report Rejected',
            message=f'Report #{report_id} telah di-reject.' + (f' Alasan: {rejection_notes}' if rejection_notes else ''),
            data={
                'report_id': report_id,
                'notes': rejection_notes
            }
        )
    except Exception as e:
        logger.warning(f"Failed to create notification for rejected report: {e}")
    
    # Update Google Sheets if available
    try:
        from google_sheets_service import GoogleSheetsService
        gs_service = GoogleSheetsService()
        if gs_service.is_available():
            headers = ['nama_user', 'link_video', 'tanggal_upload', 'tiktok_akun', 'status', 'created_at']
            sheet = gs_service.ensure_sheet_exists('laporan', headers)
            if not sheet:
                logger.warning("Sheet 'laporan' tidak bisa diakses untuk update status")
            else:
                all_values = sheet.get_all_values()
                if len(all_values) > 1:
                    sheet_headers = all_values[0]
                    # Find status column index
                    status_col_idx = None
                    for i, h in enumerate(sheet_headers):
                        if h.lower().strip() == 'status':
                            status_col_idx = i + 1  # gspread uses 1-based indexing
                            break
                    
                    if status_col_idx:
                        # Find row by link_video
                        link_col_idx = None
                        for i, h in enumerate(sheet_headers):
                            if h.lower().strip() in ['link_video', 'link video']:
                                link_col_idx = i + 1
                                break
                        
                        if link_col_idx:
                            for idx, row in enumerate(all_values[1:], start=2):
                                if len(row) >= link_col_idx and row[link_col_idx - 1] == content.link_video:
                                    sheet.update_cell(idx, status_col_idx, 'rejected')
                                    logger.info(f"Updated report status to 'rejected' in Google Sheets")
                                    break
    except Exception as e:
        logger.warning(f"Failed to update Google Sheets: {e}")
    
    db.session.commit()
    return jsonify({'message': 'Report berhasil direject'}), 200

# ==================== COMMISSIONS ====================
@app.route('/api/commissions', methods=['GET'])
@jwt_required()
def get_commissions():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    
    if user.role == 'owner':
        commissions = Commission.query.all()
    elif user.role == 'manager':
        team = Team.query.filter_by(manager_id=user_id).first()
        if team:
            member_ids = [m.user_id for m in TeamMember.query.filter_by(team_id=team.id).all()]
            commissions = Commission.query.filter(Commission.creator_id.in_(member_ids)).all()
        else:
            commissions = []
    else:
        commissions = Commission.query.filter_by(creator_id=user_id).all()
    
    return jsonify([{
        'id': c.id,
        'content_id': c.content_id,
        'product_id': c.product_id,
        'creator_id': c.creator_id,
        'creator_name': c.creator.full_name if c.creator else None,
        'total_commission': c.total_commission,
        'owner_share': c.owner_share,
        'team_share': c.team_share,
        'manager_bonus': c.manager_bonus,
        'status': c.status,
        'created_at': c.created_at.isoformat()
    } for c in commissions]), 200

@app.route('/api/commissions', methods=['POST'])
@jwt_required()
def create_commission():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa membuat komisi'}), 403
    
    data = request.json
    content = Content.query.get_or_404(data['content_id'])
    
    # Calculate commission (40% owner, 50% team, 5-10% manager)
    total_commission = data['total_commission']
    owner_share = total_commission * 0.40  # 40% owner
    team_share = total_commission * 0.50  # 50% team
    
    # Calculate manager bonus
    member = TeamMember.query.filter_by(user_id=content.creator_id).first()
    manager_bonus = 0
    if member:
        team = db.session.get(Team, member.team_id)
        if team and team.manager_id:
            manager_bonus = total_commission * (team.manager_bonus_percent / 100)
            team_share -= manager_bonus  # Reduce team share by manager bonus
    
    commission = Commission(
        content_id=data['content_id'],
        product_id=content.product_id,
        creator_id=content.creator_id,
        total_commission=total_commission,
        owner_share=owner_share,
        team_share=team_share,
        manager_bonus=manager_bonus,
        status='approved'
    )
    db.session.add(commission)
    
    # Create manager bonus record if exists
    if manager_bonus > 0 and member:
        team = db.session.get(Team, member.team_id)
        if team and team.manager_id:
            manager_bonus_record = ManagerBonus(
                manager_id=team.manager_id,
                team_id=team.id,
                commission_id=commission.id,
                bonus_amount=manager_bonus,
                status='approved'
            )
            db.session.add(manager_bonus_record)
    
    db.session.commit()
    return jsonify({'message': 'Komisi berhasil dibuat', 'id': commission.id}), 201

# ==================== PAYMENTS ====================
@app.route('/api/payments', methods=['GET'])
@jwt_required()
def get_payments():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    
    if user.role == 'owner':
        payments = Payment.query.all()
    else:
        payments = Payment.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': p.id,
        'user_id': p.user_id,
        'user_name': p.user.full_name if p.user else None,
        'amount': p.amount,
        'payment_type': p.payment_type,
        'period': p.period,
        'status': p.status,
        'created_at': p.created_at.isoformat()
    } for p in payments]), 200

@app.route('/api/payments/<int:payment_id>/mark-paid', methods=['POST'])
@jwt_required()
def mark_payment_paid(payment_id):
    """Mark payment as paid"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa mark payment as paid'}), 403
    
    payment = Payment.query.get_or_404(payment_id)
    payment.status = 'paid'
    
    db.session.commit()
    return jsonify({'message': 'Payment berhasil ditandai sebagai paid'}), 200

@app.route('/api/payments/calculate', methods=['POST'])
@jwt_required()
def calculate_payments():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa menghitung pembayaran'}), 403
    
    data = request.json
    period = data['period']  # Format: '2024-01'
    
    # Calculate team member payments
    members = TeamMember.query.all()
    payments = []
    
    for member in members:
        commissions = Commission.query.filter_by(
            creator_id=member.user_id,
            status='approved'
        ).filter(
            Commission.created_at.like(f'{period}%')
        ).all()
        
        total_team_share = sum(c.team_share for c in commissions)
        # Bonus kualitas: 10% dari komisi jika quality_score >= 8
        quality_bonus = sum(c.team_share * 0.1 for c in commissions if c.content.quality_score >= 8)
        
        if total_team_share > 0:
            payment = Payment(
                user_id=member.user_id,
                amount=total_team_share + quality_bonus,
                payment_type='commission',
                period=period,
                status='pending'
            )
            payments.append(payment)
            db.session.add(payment)
    
    # Calculate manager bonuses
    managers = User.query.filter_by(role='manager').all()
    for manager in managers:
        team = Team.query.filter_by(manager_id=manager.id).first()
        if team:
            bonuses = ManagerBonus.query.filter_by(
                manager_id=manager.id,
                status='approved'
            ).join(Commission).filter(
                Commission.created_at.like(f'{period}%')
            ).all()
            
            total_bonus = sum(b.bonus_amount for b in bonuses)
            if total_bonus > 0:
                payment = Payment(
                    user_id=manager.id,
                    amount=total_bonus,
                    payment_type='manager_bonus',
                    period=period,
                    status='pending'
                )
                payments.append(payment)
                db.session.add(payment)
    
    db.session.commit()
    return jsonify({
        'message': f'Pembayaran untuk periode {period} berhasil dihitung',
        'count': len(payments)
    }), 201

# ==================== DAILY COMMISSIONS ====================
@app.route('/api/daily-commissions', methods=['GET'])
@jwt_required()
def get_daily_commissions():
    """Get all daily commissions with pagination and filtering"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    
    # Pagination
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1
    
    try:
        per_page = int(request.args.get('per_page', 20))
        if per_page < 1:
            per_page = 20
        per_page = min(per_page, 100)
    except (ValueError, TypeError):
        per_page = 20
    
    # Filters
    date_filter = request.args.get('date', '').strip()
    user_id_filter = request.args.get('user_id', type=int)
    
    # Build query
    query = DailyCommission.query
    
    # Apply filters
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(DailyCommission.date == filter_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    if user_id_filter:
        query = query.filter(DailyCommission.user_id == user_id_filter)
    
    # Order by date desc
    query = query.order_by(DailyCommission.date.desc(), DailyCommission.created_at.desc())
    
    # Paginate
    try:
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        commissions = pagination.items
    except Exception as e:
        logger.error(f"Error paginating daily commissions: {e}", exc_info=True)
        return jsonify({'error': f'Error loading daily commissions: {str(e)}'}), 500
    
    return jsonify({
        'daily_commissions': [{
            'id': dc.id,
            'user_id': dc.user_id,
            'user_name': dc.user.full_name if dc.user else 'N/A',
            'date': dc.date.strftime('%Y-%m-%d') if dc.date else '',
            'commission_amount': float(dc.commission_amount),
            'notes': dc.notes or '',
            'updated_by': dc.updated_by,
            'updated_by_name': dc.updater.full_name if dc.updater else None,
            'created_at': dc.created_at.isoformat() if dc.created_at else None,
            'updated_at': dc.updated_at.isoformat() if dc.updated_at else None
        } for dc in commissions],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@app.route('/api/daily-commissions', methods=['POST'])
@jwt_required()
def create_daily_commission():
    """Create daily commission (owner only)"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa membuat komisi harian'}), 403
    
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON or empty request body'}), 400
    
    # Validate required fields
    if 'user_id' not in data or 'date' not in data or 'commission_amount' not in data:
        return jsonify({'error': 'user_id, date, dan commission_amount harus diisi'}), 400
    
    # Validate date
    try:
        commission_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        # Check if date is in the future
        if commission_date > datetime.now(timezone.utc).date():
            return jsonify({'error': 'Tanggal tidak boleh di masa depan'}), 400
    except ValueError:
        return jsonify({'error': 'Format tanggal tidak valid. Gunakan YYYY-MM-DD'}), 400
    
    # Validate amount
    try:
        amount = float(data['commission_amount'])
        if amount < 0:
            return jsonify({'error': 'Jumlah komisi harus >= 0'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Jumlah komisi harus berupa angka'}), 400
    
    # Check if user exists
    target_user = db.session.get(User,data['user_id'])
    if not target_user:
        return jsonify({'error': 'User tidak ditemukan'}), 404
    
    # Check if commission already exists for this user and date
    existing = DailyCommission.query.filter_by(
        user_id=data['user_id'],
        date=commission_date
    ).first()
    
    if existing:
        # Update existing
        existing.commission_amount = amount
        existing.notes = data.get('notes', '')
        existing.updated_by = user_id
        existing.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        # Update summary
        update_member_daily_summary(data['user_id'], commission_date)
        
        # Sync to Google Sheets
        sync_daily_commission_to_sheets(existing)
        
        return jsonify({
            'message': 'Komisi harian berhasil diupdate',
            'id': existing.id,
            'daily_commission': {
                'id': existing.id,
                'user_id': existing.user_id,
                'date': existing.date.strftime('%Y-%m-%d'),
                'commission_amount': float(existing.commission_amount),
                'notes': existing.notes
            }
        }), 200
    else:
        # Create new
        daily_comm = DailyCommission(
            user_id=data['user_id'],
            date=commission_date,
            commission_amount=amount,
            notes=data.get('notes', ''),
            updated_by=user_id
        )
        db.session.add(daily_comm)
        db.session.commit()
        
        # Update summary
        update_member_daily_summary(data['user_id'], commission_date)
        
        # Sync to Google Sheets
        sync_daily_commission_to_sheets(daily_comm)
        
        return jsonify({
            'message': 'Komisi harian berhasil dibuat',
            'id': daily_comm.id,
            'daily_commission': {
                'id': daily_comm.id,
                'user_id': daily_comm.user_id,
                'date': daily_comm.date.strftime('%Y-%m-%d'),
                'commission_amount': float(daily_comm.commission_amount),
                'notes': daily_comm.notes
            }
        }), 201

@app.route('/api/daily-commissions/<int:commission_id>', methods=['PUT'])
@jwt_required()
def update_daily_commission(commission_id):
    """Update daily commission (owner only)"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa mengupdate komisi harian'}), 403
    
    daily_comm = DailyCommission.query.get_or_404(commission_id)
    data = request.json
    
    # Update fields
    if 'commission_amount' in data:
        try:
            amount = float(data['commission_amount'])
            if amount < 0:
                return jsonify({'error': 'Jumlah komisi harus >= 0'}), 400
            daily_comm.commission_amount = amount
        except (ValueError, TypeError):
            return jsonify({'error': 'Jumlah komisi harus berupa angka'}), 400
    
    if 'notes' in data:
        daily_comm.notes = data['notes']
    
    if 'date' in data:
        try:
            new_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if new_date > datetime.now(timezone.utc).date():
                return jsonify({'error': 'Tanggal tidak boleh di masa depan'}), 400
            daily_comm.date = new_date
        except ValueError:
            return jsonify({'error': 'Format tanggal tidak valid. Gunakan YYYY-MM-DD'}), 400
    
    daily_comm.updated_by = user_id
    daily_comm.updated_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    # Update summary
    update_member_daily_summary(daily_comm.user_id, daily_comm.date)
    
    # Sync to Google Sheets
    sync_daily_commission_to_sheets(daily_comm)
    
    return jsonify({
        'message': 'Komisi harian berhasil diupdate',
        'daily_commission': {
            'id': daily_comm.id,
            'user_id': daily_comm.user_id,
            'date': daily_comm.date.strftime('%Y-%m-%d'),
            'commission_amount': float(daily_comm.commission_amount),
            'notes': daily_comm.notes
        }
    }), 200

@app.route('/api/daily-commissions/<int:commission_id>', methods=['DELETE'])
@jwt_required()
def delete_daily_commission(commission_id):
    """Delete daily commission (owner only)"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa menghapus komisi harian'}), 403
    
    daily_comm = DailyCommission.query.get_or_404(commission_id)
    user_id_for_summary = daily_comm.user_id
    date_for_summary = daily_comm.date
    
    db.session.delete(daily_comm)
    db.session.commit()
    
    # Update summary
    update_member_daily_summary(user_id_for_summary, date_for_summary)
    
    return jsonify({'message': 'Komisi harian berhasil dihapus'}), 200

# ==================== VIDEO STATISTICS ====================
@app.route('/api/video-statistics', methods=['GET'])
@jwt_required()
def get_video_statistics():
    """Get all video statistics with pagination and filtering"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    # Pagination
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1
    
    try:
        per_page = int(request.args.get('per_page', 20))
        if per_page < 1:
            per_page = 20
        per_page = min(per_page, 100)
    except (ValueError, TypeError):
        per_page = 20
    
    # Filters
    date_filter = request.args.get('date', '').strip()
    user_id_filter = request.args.get('user_id', type=int)
    tiktok_akun_filter = request.args.get('tiktok_akun', '').strip()
    
    # Build query
    query = VideoStatistic.query
    
    # Apply filters
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(VideoStatistic.date == filter_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    if user_id_filter:
        query = query.filter(VideoStatistic.user_id == user_id_filter)
    
    if tiktok_akun_filter:
        query = query.filter(VideoStatistic.tiktok_akun.like(f'%{tiktok_akun_filter}%'))
    
    # Order by date desc
    query = query.order_by(VideoStatistic.date.desc(), VideoStatistic.created_at.desc())
    
    # Paginate
    try:
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        statistics = pagination.items
    except Exception as e:
        logger.error(f"Error paginating video statistics: {e}", exc_info=True)
        return jsonify({'error': f'Error loading video statistics: {str(e)}'}), 500
    
    return jsonify({
        'video_statistics': [{
            'id': vs.id,
            'user_id': vs.user_id,
            'user_name': vs.user.full_name if vs.user else 'N/A',
            'tiktok_akun': vs.tiktok_akun,
            'date': vs.date.strftime('%Y-%m-%d') if vs.date else '',
            'video_count': vs.video_count,
            'total_views': vs.total_views or 0,
            'total_likes': vs.total_likes or 0,
            'updated_by': vs.updated_by,
            'updated_by_name': vs.updater.full_name if vs.updater else None,
            'created_at': vs.created_at.isoformat() if vs.created_at else None,
            'updated_at': vs.updated_at.isoformat() if vs.updated_at else None
        } for vs in statistics],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@app.route('/api/video-statistics', methods=['POST'])
@jwt_required()
def create_video_statistic():
    """Create video statistic (owner only)"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa membuat statistik video'}), 403
    
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON or empty request body'}), 400
    
    # Validate required fields
    if 'user_id' not in data or 'date' not in data or 'tiktok_akun' not in data or 'video_count' not in data:
        return jsonify({'error': 'user_id, date, tiktok_akun, dan video_count harus diisi'}), 400
    
    # Validate date
    try:
        stat_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if stat_date > datetime.now(timezone.utc).date():
            return jsonify({'error': 'Tanggal tidak boleh di masa depan'}), 400
    except ValueError:
        return jsonify({'error': 'Format tanggal tidak valid. Gunakan YYYY-MM-DD'}), 400
    
    # Validate video_count
    try:
        video_count = int(data['video_count'])
        if video_count < 0:
            return jsonify({'error': 'Jumlah video harus >= 0'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Jumlah video harus berupa angka'}), 400
    
    # Validate tiktok_akun
    tiktok_akun = data['tiktok_akun'].strip()
    if not tiktok_akun:
        return jsonify({'error': 'TikTok akun tidak boleh kosong'}), 400
    
    # Check if user exists
    target_user = db.session.get(User,data['user_id'])
    if not target_user:
        return jsonify({'error': 'User tidak ditemukan'}), 404
    
    # Check if statistic already exists
    existing = VideoStatistic.query.filter_by(
        user_id=data['user_id'],
        tiktok_akun=tiktok_akun,
        date=stat_date
    ).first()
    
    if existing:
        # Update existing
        existing.video_count = video_count
        existing.total_views = data.get('total_views', 0) or 0
        existing.total_likes = data.get('total_likes', 0) or 0
        existing.updated_by = user_id
        existing.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        # Update summary
        update_member_daily_summary(data['user_id'], stat_date)
        
        # Sync to Google Sheets
        sync_video_statistic_to_sheets(existing)
        
        return jsonify({
            'message': 'Statistik video berhasil diupdate',
            'id': existing.id,
            'video_statistic': {
                'id': existing.id,
                'user_id': existing.user_id,
                'tiktok_akun': existing.tiktok_akun,
                'date': existing.date.strftime('%Y-%m-%d'),
                'video_count': existing.video_count
            }
        }), 200
    else:
        # Create new
        video_stat = VideoStatistic(
            user_id=data['user_id'],
            tiktok_akun=tiktok_akun,
            date=stat_date,
            video_count=video_count,
            total_views=data.get('total_views', 0) or 0,
            total_likes=data.get('total_likes', 0) or 0,
            updated_by=user_id
        )
        db.session.add(video_stat)
        db.session.commit()
        
        # Update summary
        update_member_daily_summary(data['user_id'], stat_date)
        
        # Sync to Google Sheets
        sync_video_statistic_to_sheets(video_stat)
        
        return jsonify({
            'message': 'Statistik video berhasil dibuat',
            'id': video_stat.id,
            'video_statistic': {
                'id': video_stat.id,
                'user_id': video_stat.user_id,
                'tiktok_akun': video_stat.tiktok_akun,
                'date': video_stat.date.strftime('%Y-%m-%d'),
                'video_count': video_stat.video_count
            }
        }), 201

@app.route('/api/video-statistics/<int:statistic_id>', methods=['PUT'])
@jwt_required()
def update_video_statistic(statistic_id):
    """Update video statistic (owner only)"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa mengupdate statistik video'}), 403
    
    video_stat = VideoStatistic.query.get_or_404(statistic_id)
    data = request.json
    
    # Update fields
    if 'video_count' in data:
        try:
            count = int(data['video_count'])
            if count < 0:
                return jsonify({'error': 'Jumlah video harus >= 0'}), 400
            video_stat.video_count = count
        except (ValueError, TypeError):
            return jsonify({'error': 'Jumlah video harus berupa angka'}), 400
    
    if 'total_views' in data:
        video_stat.total_views = int(data.get('total_views', 0)) or 0
    
    if 'total_likes' in data:
        video_stat.total_likes = int(data.get('total_likes', 0)) or 0
    
    if 'tiktok_akun' in data:
        tiktok_akun = data['tiktok_akun'].strip()
        if not tiktok_akun:
            return jsonify({'error': 'TikTok akun tidak boleh kosong'}), 400
        video_stat.tiktok_akun = tiktok_akun
    
    if 'date' in data:
        try:
            new_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if new_date > datetime.now(timezone.utc).date():
                return jsonify({'error': 'Tanggal tidak boleh di masa depan'}), 400
            video_stat.date = new_date
        except ValueError:
            return jsonify({'error': 'Format tanggal tidak valid. Gunakan YYYY-MM-DD'}), 400
    
    video_stat.updated_by = user_id
    video_stat.updated_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    # Update summary
    update_member_daily_summary(video_stat.user_id, video_stat.date)
    
    # Sync to Google Sheets
    sync_video_statistic_to_sheets(video_stat)
    
    return jsonify({
        'message': 'Statistik video berhasil diupdate',
        'video_statistic': {
            'id': video_stat.id,
            'user_id': video_stat.user_id,
            'tiktok_akun': video_stat.tiktok_akun,
            'date': video_stat.date.strftime('%Y-%m-%d'),
            'video_count': video_stat.video_count
        }
    }), 200

@app.route('/api/video-statistics/<int:statistic_id>', methods=['DELETE'])
@jwt_required()
def delete_video_statistic(statistic_id):
    """Delete video statistic (owner only)"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa menghapus statistik video'}), 403
    
    video_stat = VideoStatistic.query.get_or_404(statistic_id)
    user_id_for_summary = video_stat.user_id
    date_for_summary = video_stat.date
    
    db.session.delete(video_stat)
    db.session.commit()
    
    # Update summary
    update_member_daily_summary(user_id_for_summary, date_for_summary)
    
    return jsonify({'message': 'Statistik video berhasil dihapus'}), 200

@app.route('/api/video-statistics/auto-sync', methods=['POST'])
@jwt_required()
def auto_sync_video_statistics():
    """Auto-sync video statistics from content table (owner only)"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa auto-sync statistik video'}), 403
    
    data = request.json or {}
    date_filter = data.get('date')  # Optional: sync for specific date
    
    try:
        # Get all content with link_video and tanggal_upload
        query = Content.query.filter(
            Content.link_video.isnot(None),
            Content.link_video != '',
            Content.tanggal_upload.isnot(None)
        )
        
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                query = query.filter(Content.tanggal_upload == filter_date)
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        contents = query.all()
        
        # Group by user_id, tiktok_akun, and tanggal_upload
        stats_dict = {}
        for content in contents:
            if not content.tiktok_akun:
                continue
            
            key = (content.creator_id, content.tiktok_akun, content.tanggal_upload)
            if key not in stats_dict:
                stats_dict[key] = 0
            stats_dict[key] += 1
        
        # Create or update video statistics
        created_count = 0
        updated_count = 0
        
        for (user_id_key, tiktok_akun, upload_date), video_count in stats_dict.items():
            existing = VideoStatistic.query.filter_by(
                user_id=user_id_key,
                tiktok_akun=tiktok_akun,
                date=upload_date
            ).first()
            
            if existing:
                existing.video_count = video_count
                existing.updated_by = user_id
                existing.updated_at = datetime.now(timezone.utc)
                updated_count += 1
            else:
                video_stat = VideoStatistic(
                    user_id=user_id_key,
                    tiktok_akun=tiktok_akun,
                    date=upload_date,
                    video_count=video_count,
                    updated_by=user_id
                )
                db.session.add(video_stat)
                created_count += 1
            
            # Update summary
            update_member_daily_summary(user_id_key, upload_date)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Auto-sync berhasil',
            'created': created_count,
            'updated': updated_count,
            'total': len(stats_dict)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in auto-sync video statistics: {e}", exc_info=True)
        return jsonify({'error': f'Error saat auto-sync: {str(e)}'}), 500

# ==================== MEMBER DAILY SUMMARY ====================
@app.route('/api/member-daily-summary', methods=['GET'])
@jwt_required()
def get_member_daily_summary():
    """Get member daily summary with filtering"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    # Filters
    date_filter = request.args.get('date', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    user_id_filter = request.args.get('user_id', type=int)
    
    # Build query
    query = MemberDailySummary.query
    
    # Apply filters
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(MemberDailySummary.date == filter_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(MemberDailySummary.date >= from_date)
        except ValueError:
            return jsonify({'error': 'Invalid date_from format. Use YYYY-MM-DD'}), 400
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(MemberDailySummary.date <= to_date)
        except ValueError:
            return jsonify({'error': 'Invalid date_to format. Use YYYY-MM-DD'}), 400
    
    if user_id_filter:
        query = query.filter(MemberDailySummary.user_id == user_id_filter)
    
    # Order by date desc
    query = query.order_by(MemberDailySummary.date.desc(), MemberDailySummary.user_id)
    
    summaries = query.all()
    
    return jsonify({
        'summaries': [{
            'id': s.id,
            'user_id': s.user_id,
            'user_name': s.user.full_name if s.user else 'N/A',
            'date': s.date.strftime('%Y-%m-%d') if s.date else '',
            'total_commission': float(s.total_commission),
            'total_videos': s.total_videos,
            'total_akun': s.total_akun,
            'updated_at': s.updated_at.isoformat() if s.updated_at else None
        } for s in summaries]
    }), 200

# ==================== HELPER FUNCTIONS ====================
def update_member_daily_summary(user_id: int, target_date: date):
    """Update or create member daily summary for a specific user and date"""
    try:
        # Get total commission for this user and date
        daily_comm = DailyCommission.query.filter_by(
            user_id=user_id,
            date=target_date
        ).first()
        total_commission = float(daily_comm.commission_amount) if daily_comm else 0.0
        
        # Get video statistics for this user and date
        video_stats = VideoStatistic.query.filter_by(
            user_id=user_id,
            date=target_date
        ).all()
        total_videos = sum(vs.video_count for vs in video_stats)
        total_akun = len(set(vs.tiktok_akun for vs in video_stats))
        
        # Get or create summary
        summary = MemberDailySummary.query.filter_by(
            user_id=user_id,
            date=target_date
        ).first()
        
        if summary:
            summary.total_commission = total_commission
            summary.total_videos = total_videos
            summary.total_akun = total_akun
            summary.updated_at = datetime.now(timezone.utc)
        else:
            summary = MemberDailySummary(
                user_id=user_id,
                date=target_date,
                total_commission=total_commission,
                total_videos=total_videos,
                total_akun=total_akun
            )
            db.session.add(summary)
        
        db.session.commit()
        logger.debug(f"Updated summary for user {user_id} on {target_date}")
        
    except Exception as e:
        logger.error(f"Error updating member daily summary: {e}", exc_info=True)
        db.session.rollback()

def sync_daily_commission_to_sheets(daily_comm: DailyCommission):
    """Sync daily commission to Google Sheets"""
    try:
        from google_sheets_service import GoogleSheetsService
        gs_service = GoogleSheetsService()
        if not gs_service.is_available():
            return
        
        headers = ['tanggal', 'user_id', 'nama_user', 'komisi', 'catatan', 'updated_by', 'updated_at']
        sheet = gs_service.ensure_sheet_exists('komisi_harian', headers)
        if not sheet:
            return
        
        # Check if row exists (by tanggal, user_id)
        all_values = sheet.get_all_values()
        if len(all_values) > 1:
            sheet_headers = all_values[0]
            date_col_idx = sheet_headers.index('tanggal') + 1 if 'tanggal' in sheet_headers else None
            user_col_idx = sheet_headers.index('user_id') + 1 if 'user_id' in sheet_headers else None
            
            if date_col_idx and user_col_idx:
                for idx, row in enumerate(all_values[1:], start=2):
                    if (len(row) >= max(date_col_idx, user_col_idx) and
                        row[date_col_idx - 1] == daily_comm.date.strftime('%Y-%m-%d') and
                        row[user_col_idx - 1] == str(daily_comm.user_id)):
                        # Update existing row
                        row_data = [
                            daily_comm.date.strftime('%Y-%m-%d'),
                            str(daily_comm.user_id),
                            daily_comm.user.full_name if daily_comm.user else 'N/A',
                            str(daily_comm.commission_amount),
                            daily_comm.notes or '',
                            daily_comm.updater.full_name if daily_comm.updater else '',
                            daily_comm.updated_at.strftime('%Y-%m-%d %H:%M:%S') if daily_comm.updated_at else ''
                        ]
                        sheet.update(f'A{idx}:G{idx}', [row_data])
                        logger.info(f"Updated daily commission in Google Sheets: row {idx}")
                        return
        
        # Add new row
        row_data = [
            daily_comm.date.strftime('%Y-%m-%d'),
            str(daily_comm.user_id),
            daily_comm.user.full_name if daily_comm.user else 'N/A',
            str(daily_comm.commission_amount),
            daily_comm.notes or '',
            daily_comm.updater.full_name if daily_comm.updater else '',
            daily_comm.updated_at.strftime('%Y-%m-%d %H:%M:%S') if daily_comm.updated_at else ''
        ]
        sheet.append_row(row_data)
        logger.info(f"Added daily commission to Google Sheets")
        
    except Exception as e:
        logger.warning(f"Failed to sync daily commission to Google Sheets: {e}")

def sync_video_statistic_to_sheets(video_stat: VideoStatistic):
    """Sync video statistic to Google Sheets"""
    try:
        from google_sheets_service import GoogleSheetsService
        gs_service = GoogleSheetsService()
        if not gs_service.is_available():
            return
        
        headers = ['tanggal', 'user_id', 'nama_user', 'tiktok_akun', 'jumlah_video', 'total_views', 'total_likes', 'updated_by', 'updated_at']
        sheet = gs_service.ensure_sheet_exists('statistik_video', headers)
        if not sheet:
            return
        
        # Check if row exists (by tanggal, user_id, tiktok_akun)
        all_values = sheet.get_all_values()
        if len(all_values) > 1:
            sheet_headers = all_values[0]
            date_col_idx = sheet_headers.index('tanggal') + 1 if 'tanggal' in sheet_headers else None
            user_col_idx = sheet_headers.index('user_id') + 1 if 'user_id' in sheet_headers else None
            akun_col_idx = sheet_headers.index('tiktok_akun') + 1 if 'tiktok_akun' in sheet_headers else None
            
            if date_col_idx and user_col_idx and akun_col_idx:
                for idx, row in enumerate(all_values[1:], start=2):
                    if (len(row) >= max(date_col_idx, user_col_idx, akun_col_idx) and
                        row[date_col_idx - 1] == video_stat.date.strftime('%Y-%m-%d') and
                        row[user_col_idx - 1] == str(video_stat.user_id) and
                        row[akun_col_idx - 1] == video_stat.tiktok_akun):
                        # Update existing row
                        row_data = [
                            video_stat.date.strftime('%Y-%m-%d'),
                            str(video_stat.user_id),
                            video_stat.user.full_name if video_stat.user else 'N/A',
                            video_stat.tiktok_akun,
                            str(video_stat.video_count),
                            str(video_stat.total_views or 0),
                            str(video_stat.total_likes or 0),
                            video_stat.updater.full_name if video_stat.updater else '',
                            video_stat.updated_at.strftime('%Y-%m-%d %H:%M:%S') if video_stat.updated_at else ''
                        ]
                        sheet.update(f'A{idx}:I{idx}', [row_data])
                        logger.info(f"Updated video statistic in Google Sheets: row {idx}")
                        return
        
        # Add new row
        row_data = [
            video_stat.date.strftime('%Y-%m-%d'),
            str(video_stat.user_id),
            video_stat.user.full_name if video_stat.user else 'N/A',
            video_stat.tiktok_akun,
            str(video_stat.video_count),
            str(video_stat.total_views or 0),
            str(video_stat.total_likes or 0),
            video_stat.updater.full_name if video_stat.updater else '',
            video_stat.updated_at.strftime('%Y-%m-%d %H:%M:%S') if video_stat.updated_at else ''
        ]
        sheet.append_row(row_data)
        logger.info(f"Added video statistic to Google Sheets")
        
    except Exception as e:
        logger.warning(f"Failed to sync video statistic to Google Sheets: {e}")

# ==================== PRODUCT SCRAPING ====================
# TikTok API Token (ensembledata.com)
TIKTOK_API_TOKEN = os.getenv('ENSEMBLEDATA_API_TOKEN', 'ZX7zQIG90hgyvvYP')

@app.route('/api/products/scrape-tiktok', methods=['POST'])
@jwt_required()
def scrape_tiktok_product():
    """Scrape produk dari TikTok Shop menggunakan ensembledata.com API"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        tiktok_url = data.get('tiktok_url', '').strip()
        if not tiktok_url:
            return jsonify({'error': 'TikTok URL harus diisi'}), 400
        
        # Extract product ID atau video ID dari URL
        product_id = None
        video_id = None
        
        # Pattern untuk TikTok URL
        # https://www.tiktok.com/@username/video/1234567890
        # https://vm.tiktok.com/xxxxx/
        video_match = re.search(r'/video/(\d+)', tiktok_url)
        if video_match:
            video_id = video_match.group(1)
        
        # Pattern untuk TikTok Shop product
        product_match = re.search(r'product[_-]?id[=:](\d+)', tiktok_url, re.IGNORECASE)
        if product_match:
            product_id = product_match.group(1)
        
        if not video_id and not product_id:
            return jsonify({'error': 'Tidak dapat mengekstrak product ID atau video ID dari URL TikTok'}), 400
        
        extracted_data = {}
        
        # Try to get product info from TikTok API
        try:
            # Call ensembledata.com API
            # Endpoint untuk product info
            api_url = "https://ensembledata.com/apis/tt/product/info"
            params = {
                "token": TIKTOK_API_TOKEN
            }
            
            if product_id:
                params["product_id"] = product_id
            elif video_id:
                params["video_id"] = video_id
                # Try to get product from video
                api_url = "https://ensembledata.com/apis/tt/video/info"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            logger.info(f"Calling TikTok API: {api_url} with params: {params}")
            response = requests.get(api_url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                api_data = response.json()
                logger.info(f"TikTok API response: {api_data}")
                
                # Parse response berdasarkan struktur API ensembledata.com
                # Adjust sesuai dengan response structure yang sebenarnya
                if 'data' in api_data:
                    product_data = api_data['data']
                elif 'product' in api_data:
                    product_data = api_data['product']
                else:
                    product_data = api_data
                
                # Extract product name
                extracted_data['product_name'] = (
                    product_data.get('product_name') or 
                    product_data.get('name') or 
                    product_data.get('title') or 
                    ''
                )
                
                # Extract price
                price = 0
                if 'price' in product_data:
                    price = float(product_data.get('price', 0))
                elif 'product_price' in product_data:
                    price = float(product_data.get('product_price', 0))
                elif 'current_price' in product_data:
                    price = float(product_data.get('current_price', 0))
                extracted_data['price'] = price
                
                # Extract original price
                original_price = price
                if 'original_price' in product_data:
                    original_price = float(product_data.get('original_price', price))
                extracted_data['original_price'] = original_price
                
                # Extract discount
                discount = 0
                if 'discount' in product_data:
                    discount = float(product_data.get('discount', 0))
                elif original_price > price and price > 0:
                    discount = ((original_price - price) / original_price) * 100
                extracted_data['discount_percent'] = discount
                
                # Extract description
                extracted_data['description'] = (
                    product_data.get('description') or 
                    product_data.get('product_description') or 
                    product_data.get('detail') or 
                    ''
                )
                
                # Extract category
                category = 'General'
                if 'category' in product_data:
                    cat_info = product_data['category']
                    if isinstance(cat_info, dict):
                        category = cat_info.get('name', 'General')
                    elif isinstance(cat_info, str):
                        category = cat_info
                elif 'category_name' in product_data:
                    category = product_data['category_name']
                extracted_data['category'] = category
                
                # Extract images
                images = []
                if 'images' in product_data:
                    images = product_data['images']
                elif 'product_images' in product_data:
                    images = product_data['product_images']
                elif 'image_urls' in product_data:
                    images = product_data['image_urls']
                elif 'image' in product_data:
                    images = [product_data['image']]
                extracted_data['product_images'] = json.dumps(images) if images else ''
                
                # Extract seller info
                seller_name = ''
                if 'seller' in product_data:
                    seller_info = product_data['seller']
                    if isinstance(seller_info, dict):
                        seller_name = seller_info.get('name', '')
                    elif isinstance(seller_info, str):
                        seller_name = seller_info
                elif 'shop_name' in product_data:
                    seller_name = product_data['shop_name']
                extracted_data['tiktok_seller_name'] = seller_name
                
                # Extract stock
                stock = 0
                if 'stock' in product_data:
                    stock = int(product_data.get('stock', 0))
                elif 'stock_quantity' in product_data:
                    stock = int(product_data.get('stock_quantity', 0))
                extracted_data['stock_quantity'] = stock
                
                # Extract rating
                rating = 0
                if 'rating' in product_data:
                    rating = float(product_data.get('rating', 0))
                elif 'average_rating' in product_data:
                    rating = float(product_data.get('average_rating', 0))
                extracted_data['rating'] = rating
                
                # Extract review count
                review_count = 0
                if 'review_count' in product_data:
                    review_count = int(product_data.get('review_count', 0))
                elif 'reviews' in product_data and isinstance(product_data['reviews'], list):
                    review_count = len(product_data['reviews'])
                extracted_data['review_count'] = review_count
                
                # Set TikTok product ID
                if product_id:
                    extracted_data['tiktok_product_id'] = product_id
                elif video_id:
                    extracted_data['tiktok_product_id'] = video_id
                
                # Set product link
                extracted_data['product_link'] = tiktok_url
                
                # Set default category if not found
                if not extracted_data.get('category'):
                    extracted_data['category'] = 'General'
                
                return jsonify({
                    'success': True,
                    'data': extracted_data,
                    'source': 'tiktok_api'
                }), 200
            else:
                error_text = response.text[:500]
                logger.error(f"TikTok API error: {response.status_code} - {error_text}")
                return jsonify({
                    'error': f'TikTok API error: {response.status_code}',
                    'message': error_text
                }), response.status_code
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling TikTok API: {e}", exc_info=True)
            return jsonify({
                'error': f'Error calling TikTok API: {str(e)}',
                'message': 'Pastikan API token valid dan koneksi internet stabil'
            }), 500
        except Exception as e:
            logger.error(f"Error parsing TikTok API response: {e}", exc_info=True)
            return jsonify({
                'error': f'Error parsing API response: {str(e)}'
            }), 500
            
    except Exception as e:
        logger.error(f"Error in scrape_tiktok_product: {e}", exc_info=True)
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/products/extract', methods=['POST'])
@jwt_required()
def extract_product_data():
    """Extract product data from Tokopedia URL or HTML"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        url = data.get('url', '').strip()
        html = data.get('html', '').strip()
        
        if not url and not html:
            return jsonify({'error': 'URL atau HTML harus diisi'}), 400
        
        extracted_data = {}
        
        # If URL is provided but no HTML, fetch HTML from URL
        if url and not html:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://www.tokopedia.com/',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                if response.status_code == 200:
                    html = response.text
                    logger.info(f"Successfully fetched HTML from URL: {url[:100]}")
            except Exception as e:
                logger.error(f"Error fetching HTML from URL: {e}", exc_info=True)
        
        # Try to extract from embedded JSON data in HTML (Tokopedia stores data in script tags)
        if html:
            try:
                # Look for JSON data in script tags
                json_patterns = [
                    r'window\.__NEXT_DATA__\s*=\s*({.+?});',
                    r'window\.__INITIAL_STATE__\s*=\s*({.+?});',
                    r'<script[^>]*>.*?("productData"\s*:\s*{.+?}).*?</script>',
                    r'<script[^>]*>.*?("pdpData"\s*:\s*{.+?}).*?</script>',
                ]
                
                for pattern in json_patterns:
                    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
                    for match in matches:
                        try:
                            json_data = json.loads(match)
                            
                            # Try to find product data in nested structure
                            def find_product_data(obj, path=[]):
                                if isinstance(obj, dict):
                                    # Check for common product data keys
                                    if 'product' in obj:
                                        return obj['product']
                                    if 'data' in obj and isinstance(obj['data'], dict):
                                        if 'basic' in obj['data'] or 'name' in obj['data']:
                                            return obj['data']
                                    if 'basic' in obj:
                                        return obj
                                    # Recursively search
                                    for key, value in obj.items():
                                        result = find_product_data(value, path + [key])
                                        if result:
                                            return result
                                elif isinstance(obj, list):
                                    for item in obj:
                                        result = find_product_data(item, path)
                                        if result:
                                            return result
                                return None
                            
                            product_data = find_product_data(json_data)
                            if product_data:
                                # Extract name
                                if 'name' in product_data:
                                    extracted_data['product_name'] = product_data['name']
                                elif 'basic' in product_data and 'name' in product_data['basic']:
                                    extracted_data['product_name'] = product_data['basic']['name']
                                
                                # Extract price
                                if 'price' in product_data:
                                    price_info = product_data['price']
                                    if isinstance(price_info, dict):
                                        extracted_data['price'] = float(price_info.get('value', price_info.get('current_price', 0)))
                                    elif isinstance(price_info, (int, float)):
                                        extracted_data['price'] = float(price_info)
                                
                                # Extract category
                                if 'category' in product_data:
                                    cat_info = product_data['category']
                                    if isinstance(cat_info, dict):
                                        extracted_data['category'] = cat_info.get('name', 'General')
                                    elif isinstance(cat_info, list) and len(cat_info) > 0:
                                        extracted_data['category'] = cat_info[-1].get('name', 'General')
                                
                                # Extract description
                                if 'description' in product_data:
                                    extracted_data['description'] = product_data['description']
                                elif 'basic' in product_data and 'description' in product_data['basic']:
                                    extracted_data['description'] = product_data['basic']['description']
                                
                                if extracted_data.get('product_name'):
                                    extracted_data['product_link'] = url or ''
                                    if 'category' not in extracted_data or not extracted_data['category']:
                                        extracted_data['category'] = 'General'
                                    
                                    return jsonify({
                                        'success': True,
                                        'data': extracted_data,
                                        'source': 'embedded_json'
                                    }), 200
                        except (json.JSONDecodeError, ValueError) as e:
                            continue
            except Exception as e:
                logger.error(f"Error extracting from embedded JSON: {e}", exc_info=True)
        
        # If HTML is provided or fetched, try HTML parsing
        if html:
            try:
                if not BeautifulSoup:
                    return jsonify({'error': 'BeautifulSoup4 tidak terinstall. Install dengan: pip install beautifulsoup4'}), 500
                soup = BeautifulSoup(html, 'html.parser')
                
                # Try to extract product name - more comprehensive selectors
                name_selectors = [
                    'h1[data-testid="lblPDPDetailProductName"]',
                    'h1[data-unify="Typography"]',
                    'h1.css-1os9jjn',
                    'h1.product-title',
                    'h1.pdp-product-name',
                    'h1[class*="product-name"]',
                    'h1[class*="ProductName"]',
                    'h1',
                    '[data-testid="lblPDPDetailProductName"]',
                    '[data-unify="Typography"]',
                    '.product-title',
                    '.pdp-product-name',
                    '[class*="product-name"]',
                    '[class*="ProductName"]',
                    'title'
                ]
                for selector in name_selectors:
                    try:
                        element = soup.select_one(selector)
                        if element:
                            name = element.get_text(strip=True)
                            if name and len(name) > 5 and name != 'Tokopedia':
                                extracted_data['product_name'] = name
                                break
                    except:
                        continue
                
                # Try to extract price - more comprehensive selectors
                price_selectors = [
                    '[data-testid="lblPDPDetailProductPrice"]',
                    '[data-unify="Typography"][class*="price"]',
                    '.price',
                    '.pdp-product-price',
                    '[class*="price"]',
                    '[class*="Price"]',
                    '[data-testid*="price"]',
                    'span[class*="price"]',
                    'div[class*="price"]'
                ]
                for selector in price_selectors:
                    try:
                        element = soup.select_one(selector)
                        if element:
                            price_text = re.sub(r'[^\d]', '', element.get_text())
                            if price_text and len(price_text) >= 4:  # At least 4 digits
                                price = int(price_text)
                                if price > 1000:  # Reasonable minimum price
                                    extracted_data['price'] = price
                                    break
                    except:
                        continue
                
                # Try to extract category - more comprehensive selectors
                category_selectors = [
                    '[data-testid*="category"]',
                    '[data-unify*="category"]',
                    '.category',
                    '.pdp-category',
                    '[class*="category"]',
                    '[class*="Category"]',
                    'a[href*="/category/"]',
                    'nav[aria-label*="breadcrumb"] a',
                    'ol[class*="breadcrumb"] a'
                ]
                for selector in category_selectors:
                    try:
                        elements = soup.select(selector)
                        for element in elements:
                            cat_text = element.get_text(strip=True)
                            if cat_text and len(cat_text) > 2 and cat_text.lower() not in ['home', 'beranda', 'tokopedia']:
                                extracted_data['category'] = cat_text
                                break
                        if 'category' in extracted_data:
                            break
                    except:
                        continue
                
                # Set default category if not found
                if 'category' not in extracted_data or not extracted_data['category']:
                    extracted_data['category'] = 'General'
                
                # Extract description - more comprehensive selectors
                desc_selectors = [
                    '[data-testid*="description"]',
                    '[data-unify*="description"]',
                    '.description',
                    '.pdp-product-description',
                    '[class*="description"]',
                    '[class*="Description"]',
                    'meta[name="description"]',
                    'meta[property="og:description"]'
                ]
                for selector in desc_selectors:
                    try:
                        element = soup.select_one(selector)
                        if element:
                            desc = element.get('content') or element.get_text(strip=True)
                            if desc and len(desc) > 10:
                                extracted_data['description'] = desc
                                break
                    except:
                        continue
                
                # Set product link
                if url:
                    extracted_data['product_link'] = url
                elif not extracted_data.get('product_link'):
                    extracted_data['product_link'] = ''
                
                # Return if we got at least name or price
                if extracted_data.get('product_name') or extracted_data.get('price'):
                    return jsonify({
                        'success': True,
                        'data': extracted_data,
                        'source': 'html_parsing'
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Tidak dapat mengekstrak data produk dari HTML. Pastikan HTML lengkap atau coba paste URL produk Tokopedia.',
                        'data': extracted_data
                    }), 400
            except Exception as e:
                logger.error(f"Error parsing HTML: {e}", exc_info=True)
                return jsonify({
                    'success': False,
                    'error': f'Error parsing HTML: {str(e)}',
                    'data': extracted_data
                }), 500
        
        # If we reach here, nothing worked
        return jsonify({
            'success': False,
            'error': 'Tidak dapat mengekstrak data produk. Pastikan URL valid atau HTML lengkap.',
            'data': extracted_data
        }), 400
        
    except Exception as e:
        logger.error(f"Error in extract_product_data: {e}", exc_info=True)
        return jsonify({'error': f'Error extracting product data: {str(e)}'}), 500

# ==================== AI TOOLS ====================
@app.route('/api/ai/generate-content', methods=['POST'])
@jwt_required()
def generate_content():
    data = request.json
    product = Product.query.get_or_404(data['product_id'])
    
    # Template-based content generator
    templates = {
        'tiktok': {
            'title': f"Review {product.title} - Wajib Coba! 🔥",
            'description': f"Produk {product.title} dari kategori {product.category} dengan komisi menarik. Link di bio!",
            'hashtags': f"#{product.category.replace(' ', '')} #affiliate #review #tiktok"
        },
        'shopee': {
            'title': f"Promo {product.title} - Harga Terbaik!",
            'description': f"Dapatkan {product.title} dengan harga terbaik. Klik link di bio untuk beli sekarang!",
            'hashtags': f"#{product.category.replace(' ', '')} #shopee #promo #affiliate"
        }
    }
    
    platform = data.get('platform', 'tiktok')
    template = templates.get(platform, templates['tiktok'])
    
    return jsonify(template), 200

# ==================== GOOGLE SHEETS SYNC ====================
@app.route('/api/google-sheets/sync', methods=['POST'])
@jwt_required()
def sync_google_sheets():
    """Sync data from Google Sheets to database"""
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    if user.role != 'owner':
        return jsonify({'error': 'Hanya owner yang bisa sync Google Sheets'}), 403
    
    try:
        from google_sheets_service import GoogleSheetsService
        gs_service = GoogleSheetsService()
        
        if not gs_service.is_available():
            return jsonify({'error': 'Google Sheets service tidak tersedia. Pastikan google_credentials.json ada dan valid.'}), 503
        
        # Sync all data
        logger.info("Starting Google Sheets sync...")
        results = gs_service.sync_all_from_sheets()
        
        # Get sync results
        synced_items = []
        if results.get('products', False):
            synced_items.append('products')
        if results.get('users', False):
            synced_items.append('users')
        if results.get('reports', False):
            synced_items.append('reports')
        
        # Get counts after sync to verify
        product_count = Product.query.count()
        user_count = User.query.filter(User.role == 'member').count()
        report_count = Content.query.filter(
            Content.link_video != None,
            Content.link_video != ''
        ).count()
        
        logger.info(f"Google Sheets sync completed. Products: {product_count}, Users: {user_count}, Reports: {report_count}")
        
        if all(results.values()):
            logger.info("Google Sheets sync completed successfully")
            return jsonify({
                'message': 'Sync berhasil! Data dari Google Sheets sudah di-update ke database.',
                'synced': synced_items,
                'counts': {
                    'products': product_count,
                    'users': user_count,
                    'reports': report_count
                }
            }), 200
        else:
            logger.warning("Google Sheets sync completed with some errors")
            return jsonify({
                'message': 'Sync selesai dengan beberapa error. Cek log untuk detail.',
                'synced': synced_items,
                'counts': {
                    'products': product_count,
                    'users': user_count,
                    'reports': report_count
                }
            }), 200
    except Exception as e:
        logger.error(f"Error syncing Google Sheets: {e}", exc_info=True)
        return jsonify({'error': f'Error saat sync: {str(e)}'}), 500

# ==================== DASHBOARD STATS ====================
@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = db.session.get(User, user_id)
    
    # Get date filters from query parameters
    date_from_str = request.args.get('date_from', '').strip()
    date_to_str = request.args.get('date_to', '').strip()
    
    date_from = None
    date_to = None
    
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        except ValueError:
            logger.warning(f"Invalid date_from format: {date_from_str}")
    
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            logger.warning(f"Invalid date_to format: {date_to_str}")
    
    # Build date filter for queries
    date_filter = None
    if date_from and date_to:
        date_filter = (date_from, date_to)
    elif date_from:
        date_filter = (date_from, None)
    elif date_to:
        date_filter = (None, date_to)
    
    if user.role == 'owner':
        # Helper function to apply date filter to query
        def apply_date_filter(query, date_column):
            if date_filter:
                date_from_val, date_to_val = date_filter
                if date_from_val:
                    query = query.filter(date_column >= datetime.combine(date_from_val, datetime.min.time()).replace(tzinfo=timezone.utc))
                if date_to_val:
                    # Include the entire day
                    query = query.filter(date_column <= datetime.combine(date_to_val, datetime.max.time()).replace(tzinfo=timezone.utc))
            return query
        
        # Basic counts
        total_users = User.query.filter(User.role == 'member').count()
        
        # Active users - use date filter if provided, otherwise default to 30 days
        active_users_query = User.query.filter(User.role == 'member')
        if date_filter:
            active_users_query = apply_date_filter(active_users_query, User.created_at)
        else:
            active_users_query = active_users_query.filter(
                User.created_at >= datetime.now(timezone.utc) - timedelta(days=30)
            )
        active_users = active_users_query.count()
        
        # Total videos - apply date filter if provided
        total_videos_query = Content.query.filter(Content.link_video.isnot(None))
        if date_filter:
            total_videos_query = apply_date_filter(total_videos_query, Content.created_at)
        total_videos = total_videos_query.count()
        
        # Videos this month - use date filter if provided, otherwise default to this month
        videos_this_month_query = Content.query.filter(Content.link_video.isnot(None))
        if date_filter:
            videos_this_month_query = apply_date_filter(videos_this_month_query, Content.created_at)
        else:
            videos_this_month_query = videos_this_month_query.filter(
                Content.created_at >= datetime.now(timezone.utc).replace(day=1)
            )
        videos_this_month = videos_this_month_query.count()
        
        # Content status - apply date filter if provided
        pending_videos_query = Content.query.filter_by(status='pending')
        approved_videos_query = Content.query.filter_by(status='approved')
        rejected_videos_query = Content.query.filter_by(status='rejected')
        
        if date_filter:
            pending_videos_query = apply_date_filter(pending_videos_query, Content.created_at)
            approved_videos_query = apply_date_filter(approved_videos_query, Content.created_at)
            rejected_videos_query = apply_date_filter(rejected_videos_query, Content.created_at)
        
        pending_videos = pending_videos_query.count()
        approved_videos = approved_videos_query.count()
        rejected_videos = rejected_videos_query.count()
        
        # Approval rate
        total_reviewed = approved_videos + rejected_videos
        approval_rate = (approved_videos / total_reviewed * 100) if total_reviewed > 0 else 0
        
        # Quality scores - apply date filter if provided
        quality_query = Content.query.filter(Content.quality_score > 0)
        if date_filter:
            quality_query = apply_date_filter(quality_query, Content.created_at)
        
        avg_quality_score_query = db.session.query(func.avg(Content.quality_score)).filter(
            Content.quality_score > 0
        )
        if date_filter:
            avg_quality_score_query = apply_date_filter(avg_quality_score_query, Content.created_at)
        avg_quality_score = avg_quality_score_query.scalar() or 0
        
        high_quality_videos_query = Content.query.filter(Content.quality_score >= 8)
        if date_filter:
            high_quality_videos_query = apply_date_filter(high_quality_videos_query, Content.created_at)
        high_quality_videos = high_quality_videos_query.count()
        
        # Commissions - apply date filter if provided
        total_commissions_query = db.session.query(func.sum(Commission.total_commission))
        owner_earnings_query = db.session.query(func.sum(Commission.owner_share))
        team_earnings_query = db.session.query(func.sum(Commission.team_share))
        pending_commissions_query = db.session.query(func.sum(Commission.total_commission)).filter_by(status='pending')
        
        if date_filter:
            total_commissions_query = apply_date_filter(total_commissions_query, Commission.created_at)
            owner_earnings_query = apply_date_filter(owner_earnings_query, Commission.created_at)
            team_earnings_query = apply_date_filter(team_earnings_query, Commission.created_at)
            pending_commissions_query = apply_date_filter(pending_commissions_query, Commission.created_at)
        
        total_commissions = total_commissions_query.scalar() or 0
        owner_earnings = owner_earnings_query.scalar() or 0
        team_earnings = team_earnings_query.scalar() or 0
        pending_commissions = pending_commissions_query.scalar() or 0
        
        # Teams
        total_teams = Team.query.count()
        total_members = TeamMember.query.count()
        
        # Top performers (by commission) - apply date filter if provided
        top_earners_query = db.session.query(
            User.id,
            User.full_name,
            func.sum(Commission.team_share).label('total_earnings')
        ).join(Commission, User.id == Commission.creator_id).filter(
            Commission.status.in_(['approved', 'paid'])
        )
        if date_filter:
            top_earners_query = apply_date_filter(top_earners_query, Commission.created_at)
        top_earners = top_earners_query.group_by(User.id, User.full_name).order_by(
            func.sum(Commission.team_share).desc()
        ).limit(5).all()
        
        top_earners_list = [{
            'id': u.id,
            'name': u.full_name or 'Unknown',
            'earnings': float(total)
        } for u, total in top_earners]
        
        # Top videos (by quality score) - apply date filter if provided
        top_videos_query = Content.query.filter(Content.quality_score > 0)
        if date_filter:
            top_videos_query = apply_date_filter(top_videos_query, Content.created_at)
        top_videos = top_videos_query.order_by(Content.quality_score.desc()).limit(5).all()
        
        top_videos_list = [{
            'id': c.id,
            'title': c.title or 'No title',
            'creator': c.creator.full_name if c.creator else 'Unknown',
            'score': float(c.quality_score),
            'link': c.link_video or ''
        } for c in top_videos]
        
        # Recent activity - use date filter if provided, otherwise default to last 7 days
        recent_videos_query = Content.query
        recent_users_query = User.query.filter(User.role == 'member')
        if date_filter:
            recent_videos_query = apply_date_filter(recent_videos_query, Content.created_at)
            recent_users_query = apply_date_filter(recent_users_query, User.created_at)
        else:
            recent_videos_query = recent_videos_query.filter(
                Content.created_at >= datetime.now(timezone.utc) - timedelta(days=7)
            )
            recent_users_query = recent_users_query.filter(
                User.created_at >= datetime.now(timezone.utc) - timedelta(days=7)
            )
        recent_videos = recent_videos_query.count()
        recent_users = recent_users_query.count()
        
        # Payments - apply date filter if provided
        total_payments_query = db.session.query(func.sum(Payment.amount)).filter_by(status='paid')
        pending_payments_query = db.session.query(func.sum(Payment.amount)).filter_by(status='pending')
        if date_filter:
            total_payments_query = apply_date_filter(total_payments_query, Payment.created_at)
            pending_payments_query = apply_date_filter(pending_payments_query, Payment.created_at)
        total_payments = total_payments_query.scalar() or 0
        pending_payments = pending_payments_query.scalar() or 0
        
        return jsonify({
            # User metrics
            'total_users': total_users,
            'active_users': active_users,
            'recent_users': recent_users,
            
            # Video metrics
            'total_videos': total_videos,
            'videos_this_month': videos_this_month,
            'recent_videos': recent_videos,
            'pending_videos': pending_videos,
            'approved_videos': approved_videos,
            'rejected_videos': rejected_videos,
            'approval_rate': round(approval_rate, 1),
            
            # Quality metrics
            'avg_quality_score': round(float(avg_quality_score), 1),
            'high_quality_videos': high_quality_videos,
            
            # Commission metrics
            'total_commissions': total_commissions,
            'owner_earnings': owner_earnings,
            'team_earnings': team_earnings,
            'pending_commissions': pending_commissions,
            
            # Team metrics
            'total_teams': total_teams,
            'total_members': total_members,
            
            # Payment metrics
            'total_payments': total_payments,
            'pending_payments': pending_payments,
            
            # Top performers
            'top_earners': top_earners_list,
            'top_videos': top_videos_list
        }), 200
    
    elif user.role == 'manager':
        team = Team.query.filter_by(manager_id=user_id).first()
        if team:
            member_ids = [m.user_id for m in TeamMember.query.filter_by(team_id=team.id).all()]
            total_commissions = db.session.query(func.sum(Commission.total_commission)).filter(
                Commission.creator_id.in_(member_ids)
            ).scalar() or 0
            total_bonus = db.session.query(func.sum(ManagerBonus.bonus_amount)).filter_by(
                manager_id=user_id
            ).scalar() or 0
            
            return jsonify({
                'team_name': team.name,
                'team_members': len(member_ids),
                'total_commissions': total_commissions,
                'manager_bonus': total_bonus,
                'target_commission': team.target_commission,
                'target_percentage': (total_commissions / team.target_commission * 100) if team.target_commission > 0 else 0
            }), 200
    
    else:
        total_commissions = db.session.query(func.sum(Commission.team_share)).filter_by(
            creator_id=user_id
        ).scalar() or 0
        total_content = Content.query.filter_by(creator_id=user_id).count()
        approved_content = Content.query.filter_by(creator_id=user_id, status='approved').count()
        
        return jsonify({
            'total_earnings': total_commissions,
            'total_content': total_content,
            'approved_content': approved_content,
            'pending_payments': db.session.query(func.sum(Payment.amount)).filter_by(
                user_id=user_id,
                status='pending'
            ).scalar() or 0
        }), 200

# ==================== STATIC FILES ====================
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('../frontend/css', path)

@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('../frontend/js', path)

# ==================== TELEGRAM BOT ====================
from telegram_bot import setup_bot
from telegram import Update
import threading
import asyncio
import time
from google_sheets_service import GoogleSheetsService
from channel_service import ChannelService

def run_bot():
    """Run Telegram bot in separate thread"""
    try:
        # Create new event loop for this thread (required for asyncio)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Clear webhook first to prevent conflict
        import requests
        token = os.getenv('TELEGRAM_TOKEN', '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE')
        try:
            # Clear webhook multiple times to ensure it's cleared
            for i in range(3):
                try:
                    response = requests.post(
                        f"https://api.telegram.org/bot{token}/deleteWebhook?drop_pending_updates=true",
                        timeout=5
                    )
                    if response.status_code == 200:
                        print("   ✅ Webhook cleared")
                        break
                except:
                    pass
            # Also try to get updates to clear any pending
            try:
                requests.post(
                    f"https://api.telegram.org/bot{token}/getUpdates?offset=-1",
                    timeout=5
                )
            except:
                pass
        except Exception as e:
            print(f"   ⚠️ Warning: Could not clear webhook: {e}")
        
        # Setup bot
        bot_app = setup_bot(app, db)
        
        print("🤖 Starting Telegram Bot...")
        print("   Clearing pending updates...")
        
        # Run polling - it will use the event loop we just created
        # drop_pending_updates=True akan skip semua pending updates
        bot_app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,  # Skip old messages saat start (PENTING!)
            close_loop=False,  # Don't close loop when stopping
            stop_signals=None  # Don't handle signals in thread
        )
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()

def run_periodic_sync():
    """Run periodic sync with Google Sheets and channel posting"""
    time.sleep(30)  # Wait for app to start
    
    # Configurable intervals via environment variables
    sync_interval = int(os.getenv('SYNC_INTERVAL', '300'))  # Default 5 minutes
    channel_interval = int(os.getenv('CHANNEL_INTERVAL', '600'))  # Default 10 minutes
    
    last_sync = 0
    last_channel_post = 0
    
    logger.info(f"Periodic sync started (sync every {sync_interval}s, channel every {channel_interval}s)")
    
    while True:
        try:
            current_time = time.time()
            
            with app.app_context():
                # Sync from Google Sheets (every SYNC_INTERVAL seconds)
                if current_time - last_sync >= sync_interval:
                    gs_service = GoogleSheetsService()
                    if gs_service.is_available():
                        logger.info("🔄 Syncing from Google Sheets...")
                        try:
                            success = gs_service.sync_all_from_sheets()
                            if success:
                                logger.info("✅ Google Sheets sync completed")
                            else:
                                logger.warning("⚠️ Google Sheets sync completed with errors")
                        except Exception as e:
                            logger.error(f"❌ Error during Google Sheets sync: {e}", exc_info=True)
                        last_sync = current_time
                
                # Post products to channel (every CHANNEL_INTERVAL seconds)
                if current_time - last_channel_post >= channel_interval:
                    channel_service = ChannelService(
                        bot_token=os.getenv('TELEGRAM_TOKEN', ''),
                        channel_id=os.getenv('CHANNEL_CHAT_ID', '-1003607323066')
                    )
                    if channel_service.bot:
                        logger.info("📢 Posting products to channel...")
                        try:
                            # Use asyncio to run async function
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            loop.run_until_complete(channel_service.post_products_summary())
                            loop.close()
                            logger.info("✅ Channel posting completed")
                        except Exception as e:
                            logger.error(f"❌ Error during channel posting: {e}", exc_info=True)
                        last_channel_post = current_time
            
            # Sleep for 1 minute, then check again
            time.sleep(60)
        
        except Exception as e:
            logger.error(f"❌ Error in periodic sync loop: {e}", exc_info=True)
            time.sleep(60)  # Wait 1 minute before retry

# ==================== API DOCUMENTATION ====================
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """API Documentation endpoint"""
    docs = {
        'version': '1.0',
        'base_url': '/api',
        'endpoints': {
            'auth': {
                'POST /api/auth/register': 'Register new user',
                'POST /api/auth/login': 'Login user'
            },
            'users': {
                'GET /api/users': 'Get all users (with pagination, search)',
                'GET /api/users?page=1&per_page=20&search=keyword': 'Pagination & search example',
                'PUT /api/users/<id>': 'Update user (owner only)'
            },
            'products': {
                'GET /api/products': 'Get all products (with pagination, filter, search)',
                'GET /api/products?status=active&category=Electronics&search=keyword': 'Filter example',
                'POST /api/products': 'Create product (owner only)',
                'PUT /api/products/<id>': 'Update product (owner only)',
                'DELETE /api/products/<id>': 'Delete product (owner only)'
            },
            'reports': {
                'GET /api/reports': 'Get all reports (with pagination, filter, search)',
                'GET /api/reports?status=pending&user_id=1&search=keyword': 'Filter example',
                'POST /api/reports/<id>/approve': 'Approve report (owner only)',
                'POST /api/reports/<id>/reject': 'Reject report (owner only)'
            },
            'health': {
                'GET /health': 'Health check endpoint',
                'GET /api/health': 'Health check endpoint (API)'
            }
        },
        'pagination': {
            'page': 'Page number (default: 1)',
            'per_page': 'Items per page (default: 20, max: 100)'
        },
        'authentication': {
            'type': 'JWT Bearer Token',
            'header': 'Authorization: Bearer <token>',
            'token_expires': '30 days'
        }
    }
    return jsonify(docs), 200

if __name__ == '__main__':
    # Start Telegram bot in background thread
    # Note: use_reloader=False prevents duplicate bot instances when Flask restarts
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("🤖 Telegram Bot started!")
    
    # Start periodic sync thread
    sync_thread = threading.Thread(target=run_periodic_sync, daemon=True)
    sync_thread.start()
    print("🔄 Periodic sync started (every 5 minutes)")
    
    # Run Flask app
    # use_reloader=False prevents bot from starting multiple times
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

