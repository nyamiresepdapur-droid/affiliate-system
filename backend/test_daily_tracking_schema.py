"""
Test script untuk verify schema Daily Tracking (Phase 1)
Jalankan: python test_daily_tracking_schema.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models import DailyCommission, VideoStatistic, MemberDailySummary, User
from datetime import date, datetime

def test_schema():
    """Test apakah schema bisa dibuat dan model bisa digunakan"""
    print("🧪 Testing Daily Tracking Schema...")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Test 1: Check if tables exist
            print("\n1. Checking if tables exist...")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['daily_commissions', 'video_statistics', 'member_daily_summary']
            for table in required_tables:
                if table in tables:
                    print(f"   ✅ Table '{table}' exists")
                else:
                    print(f"   ❌ Table '{table}' NOT found!")
                    return False
            
            # Test 2: Check table structure
            print("\n2. Checking table structure...")
            
            # Check daily_commissions
            daily_comm_columns = [col['name'] for col in inspector.get_columns('daily_commissions')]
            required_columns = ['id', 'user_id', 'date', 'commission_amount', 'notes', 'updated_by', 'created_at', 'updated_at']
            for col in required_columns:
                if col in daily_comm_columns:
                    print(f"   ✅ daily_commissions.{col} exists")
                else:
                    print(f"   ❌ daily_commissions.{col} NOT found!")
                    return False
            
            # Check video_statistics
            video_stat_columns = [col['name'] for col in inspector.get_columns('video_statistics')]
            required_columns = ['id', 'user_id', 'tiktok_akun', 'date', 'video_count', 'total_views', 'total_likes', 'updated_by', 'created_at', 'updated_at']
            for col in required_columns:
                if col in video_stat_columns:
                    print(f"   ✅ video_statistics.{col} exists")
                else:
                    print(f"   ❌ video_statistics.{col} NOT found!")
                    return False
            
            # Check member_daily_summary
            summary_columns = [col['name'] for col in inspector.get_columns('member_daily_summary')]
            required_columns = ['id', 'user_id', 'date', 'total_commission', 'total_videos', 'total_akun', 'updated_at']
            for col in required_columns:
                if col in summary_columns:
                    print(f"   ✅ member_daily_summary.{col} exists")
                else:
                    print(f"   ❌ member_daily_summary.{col} NOT found!")
                    return False
            
            # Test 3: Test model creation (without saving)
            print("\n3. Testing model creation...")
            
            # Get a test user (or create one)
            test_user = User.query.first()
            if not test_user:
                print("   ⚠️  No users found. Creating test user...")
                test_user = User(
                    username='test_user',
                    email='test@test.com',
                    password_hash='test',
                    role='member',
                    full_name='Test User'
                )
                db.session.add(test_user)
                db.session.commit()
                print("   ✅ Test user created")
            
            # Test DailyCommission model
            daily_comm = DailyCommission(
                user_id=test_user.id,
                date=date.today(),
                commission_amount=50000.0,
                notes='Test commission'
            )
            print(f"   ✅ DailyCommission model created: user_id={daily_comm.user_id}, date={daily_comm.date}, amount={daily_comm.commission_amount}")
            
            # Test VideoStatistic model
            video_stat = VideoStatistic(
                user_id=test_user.id,
                tiktok_akun='@test_account',
                date=date.today(),
                video_count=5
            )
            print(f"   ✅ VideoStatistic model created: user_id={video_stat.user_id}, akun={video_stat.tiktok_akun}, count={video_stat.video_count}")
            
            # Test MemberDailySummary model
            summary = MemberDailySummary(
                user_id=test_user.id,
                date=date.today(),
                total_commission=50000.0,
                total_videos=5,
                total_akun=1
            )
            print(f"   ✅ MemberDailySummary model created: user_id={summary.user_id}, date={summary.date}, commission={summary.total_commission}, videos={summary.total_videos}")
            
            # Test 4: Test relationships
            print("\n4. Testing relationships...")
            if hasattr(test_user, 'daily_commissions'):
                print("   ✅ User.daily_commissions relationship exists")
            else:
                print("   ❌ User.daily_commissions relationship NOT found!")
                return False
            
            if hasattr(test_user, 'video_statistics'):
                print("   ✅ User.video_statistics relationship exists")
            else:
                print("   ❌ User.video_statistics relationship NOT found!")
                return False
            
            if hasattr(test_user, 'daily_summaries'):
                print("   ✅ User.daily_summaries relationship exists")
            else:
                print("   ❌ User.daily_summaries relationship NOT found!")
                return False
            
            print("\n" + "=" * 50)
            print("✅ All tests passed! Schema is ready.")
            print("=" * 50)
            return True
            
        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = test_schema()
    sys.exit(0 if success else 1)

