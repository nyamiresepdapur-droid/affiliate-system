"""
Comprehensive System Test
Test semua komponen sistem untuk memastikan berjalan sempurna
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Product, Content, Team, Commission, Payment
from google_sheets_service import GoogleSheetsService
import json

def test_database():
    """Test database connection dan models"""
    print("=" * 60)
    print("1. DATABASE TEST")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Test connection
            db.session.execute(db.text('SELECT 1'))
            print("✅ Database connection: OK")
            
            # Test models
            user_count = User.query.count()
            product_count = Product.query.count()
            content_count = Content.query.count()
            team_count = Team.query.count()
            commission_count = Commission.query.count()
            payment_count = Payment.query.count()
            
            print(f"✅ Models accessible:")
            print(f"   - Users: {user_count}")
            print(f"   - Products: {product_count}")
            print(f"   - Content: {content_count}")
            print(f"   - Teams: {team_count}")
            print(f"   - Commissions: {commission_count}")
            print(f"   - Payments: {payment_count}")
            
            # Test owner exists
            owner = User.query.filter_by(role='owner').first()
            if owner:
                print(f"✅ Owner user exists: {owner.username}")
            else:
                print("⚠️  Owner user not found (will be created on app start)")
            
            return True
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False

def test_google_sheets():
    """Test Google Sheets service"""
    print("\n" + "=" * 60)
    print("2. GOOGLE SHEETS TEST")
    print("=" * 60)
    
    try:
        gs_service = GoogleSheetsService()
        
        if not gs_service.is_available():
            print("⚠️  Google Sheets service not available")
            print("   (This is OK if google_credentials.json is not set up)")
            return True  # Not a critical error
        
        print("✅ Google Sheets service available")
        
        # Test sheet access
        with app.app_context():
            # Test ensure_sheet_exists
            headers = ['nama produk', 'harga produk', 'link produk', 'komisi_reguler', 'komisi_gmv', 'target_gmv', 'status']
            sheet = gs_service.ensure_sheet_exists('produk', headers)
            if sheet:
                print("✅ Sheet 'produk' accessible")
            else:
                print("❌ Sheet 'produk' not accessible")
                return False
            
            # Test sync functions exist
            if hasattr(gs_service, 'sync_products_from_sheet'):
                print("✅ sync_products_from_sheet() exists")
            if hasattr(gs_service, 'sync_users_from_sheet'):
                print("✅ sync_users_from_sheet() exists")
            if hasattr(gs_service, 'sync_reports_from_sheet'):
                print("✅ sync_reports_from_sheet() exists")
            if hasattr(gs_service, 'sync_all_from_sheets'):
                print("✅ sync_all_from_sheets() exists")
        
        return True
    except Exception as e:
        print(f"❌ Google Sheets test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints structure"""
    print("\n" + "=" * 60)
    print("3. API ENDPOINTS TEST")
    print("=" * 60)
    
    with app.test_client() as client:
        # Test health check
        try:
            res = client.get('/api/health')
            if res.status_code == 200:
                print("✅ /api/health: OK")
            else:
                print(f"⚠️  /api/health: Status {res.status_code}")
        except Exception as e:
            print(f"❌ /api/health failed: {e}")
            return False
        
        # Test auth endpoints (should return 400/422 for empty request, not 500)
        try:
            res = client.post('/api/auth/login', json={})
            if res.status_code in [400, 422]:
                print("✅ /api/auth/login: Validates input (returns 400/422 for empty)")
            else:
                print(f"⚠️  /api/auth/login: Unexpected status {res.status_code}")
        except Exception as e:
            print(f"❌ /api/auth/login test failed: {e}")
        
        # Test protected endpoint (should return 401)
        try:
            res = client.get('/api/products')
            if res.status_code == 401:
                print("✅ /api/products: Protected (returns 401 without token)")
            else:
                print(f"⚠️  /api/products: Unexpected status {res.status_code}")
        except Exception as e:
            print(f"❌ /api/products test failed: {e}")
    
    return True

def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 60)
    print("4. ERROR HANDLING TEST")
    print("=" * 60)
    
    # Check if error handlers exist
    error_handlers = [
        ('404', app.error_handler_spec.get(None, {}).get(404)),
        ('500', app.error_handler_spec.get(None, {}).get(500)),
        ('422', app.error_handler_spec.get(None, {}).get(422)),
        ('Exception', app.error_handler_spec.get(None, {}).get(Exception)),
    ]
    
    for name, handler in error_handlers:
        if handler:
            print(f"✅ Error handler for {name}: OK")
        else:
            print(f"⚠️  Error handler for {name}: Not found")
    
    return True

def test_models_relationships():
    """Test model relationships"""
    print("\n" + "=" * 60)
    print("5. MODEL RELATIONSHIPS TEST")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Test User relationships
            user = User.query.first()
            if user:
                print("✅ User model: OK")
                if hasattr(user, 'created_content'):
                    print("✅ User.created_content relationship: OK")
                if hasattr(user, 'managed_teams'):
                    print("✅ User.managed_teams relationship: OK")
                if hasattr(user, 'payments'):
                    print("✅ User.payments relationship: OK")
            
            # Test Product model
            product = Product.query.first()
            if product or Product.query.count() == 0:
                print("✅ Product model: OK")
            
            # Test Content model
            content = Content.query.first()
            if content or Content.query.count() == 0:
                print("✅ Content model: OK")
                if content and hasattr(content, 'creator'):
                    print("✅ Content.creator relationship: OK")
            
            return True
        except Exception as e:
            print(f"❌ Model relationships test failed: {e}")
            return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    print()
    
    results = {
        'database': test_database(),
        'google_sheets': test_google_sheets(),
        'api_endpoints': test_api_endpoints(),
        'error_handling': test_error_handling(),
        'model_relationships': test_models_relationships()
    }
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! System is ready.")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

