"""
Test script untuk API Daily Tracking
Jalankan: python test_daily_tracking_api.py
"""

import sys
import os
import requests
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(__file__))

# Configuration
BASE_URL = 'http://localhost:5000/api'
TEST_USERNAME = 'owner'
TEST_PASSWORD = 'admin123'

def login():
    """Login dan dapatkan token"""
    print("🔐 Logging in...")
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'username': TEST_USERNAME,
        'password': TEST_PASSWORD
    })
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        print(f"✅ Login berhasil! Role: {data.get('user', {}).get('role')}")
        return token
    else:
        print(f"❌ Login gagal: {response.status_code}")
        print(response.text)
        return None

def test_daily_commissions(token):
    """Test Daily Commissions API"""
    print("\n" + "="*50)
    print("💰 Testing Daily Commissions API")
    print("="*50)
    
    headers = {'Authorization': f'Bearer {token}'}
    today = date.today().isoformat()
    
    # Test 1: Create Daily Commission
    print("\n1. Creating daily commission...")
    commission_data = {
        'user_id': 1,  # Assuming user ID 1 exists
        'date': today,
        'commission_amount': 50000.0,
        'notes': 'Test commission'
    }
    
    response = requests.post(
        f'{BASE_URL}/daily-commissions',
        json=commission_data,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        data = response.json()
        commission_id = data.get('id') or data.get('daily_commission', {}).get('id')
        print(f"   ✅ Daily commission created/updated: ID={commission_id}")
        
        # Test 2: Get Daily Commissions
        print("\n2. Getting daily commissions...")
        response = requests.get(
            f'{BASE_URL}/daily-commissions?date={today}',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            commissions = data.get('daily_commissions', [])
            print(f"   ✅ Found {len(commissions)} daily commission(s)")
            
            if commission_id:
                # Test 3: Update Daily Commission
                print("\n3. Updating daily commission...")
                update_data = {
                    'commission_amount': 75000.0,
                    'notes': 'Updated test commission'
                }
                
                response = requests.put(
                    f'{BASE_URL}/daily-commissions/{commission_id}',
                    json=update_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    print("   ✅ Daily commission updated")
                else:
                    print(f"   ❌ Update failed: {response.status_code}")
                    print(response.text)
                
                # Test 4: Delete Daily Commission
                print("\n4. Deleting daily commission...")
                response = requests.delete(
                    f'{BASE_URL}/daily-commissions/{commission_id}',
                    headers=headers
                )
                
                if response.status_code == 200:
                    print("   ✅ Daily commission deleted")
                else:
                    print(f"   ❌ Delete failed: {response.status_code}")
        else:
            print(f"   ❌ Get failed: {response.status_code}")
            print(response.text)
    else:
        print(f"   ❌ Create failed: {response.status_code}")
        print(response.text)

def test_video_statistics(token):
    """Test Video Statistics API"""
    print("\n" + "="*50)
    print("📹 Testing Video Statistics API")
    print("="*50)
    
    headers = {'Authorization': f'Bearer {token}'}
    today = date.today().isoformat()
    
    # Test 1: Create Video Statistic
    print("\n1. Creating video statistic...")
    stat_data = {
        'user_id': 1,  # Assuming user ID 1 exists
        'date': today,
        'tiktok_akun': '@test_account',
        'video_count': 5,
        'total_views': 1000,
        'total_likes': 500
    }
    
    response = requests.post(
        f'{BASE_URL}/video-statistics',
        json=stat_data,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        data = response.json()
        stat_id = data.get('id') or data.get('video_statistic', {}).get('id')
        print(f"   ✅ Video statistic created/updated: ID={stat_id}")
        
        # Test 2: Get Video Statistics
        print("\n2. Getting video statistics...")
        response = requests.get(
            f'{BASE_URL}/video-statistics?date={today}',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            statistics = data.get('video_statistics', [])
            print(f"   ✅ Found {len(statistics)} video statistic(s)")
            
            if stat_id:
                # Test 3: Update Video Statistic
                print("\n3. Updating video statistic...")
                update_data = {
                    'video_count': 10,
                    'total_views': 2000,
                    'total_likes': 1000
                }
                
                response = requests.put(
                    f'{BASE_URL}/video-statistics/{stat_id}',
                    json=update_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    print("   ✅ Video statistic updated")
                else:
                    print(f"   ❌ Update failed: {response.status_code}")
                    print(response.text)
                
                # Test 4: Delete Video Statistic
                print("\n4. Deleting video statistic...")
                response = requests.delete(
                    f'{BASE_URL}/video-statistics/{stat_id}',
                    headers=headers
                )
                
                if response.status_code == 200:
                    print("   ✅ Video statistic deleted")
                else:
                    print(f"   ❌ Delete failed: {response.status_code}")
        else:
            print(f"   ❌ Get failed: {response.status_code}")
            print(response.text)
    else:
        print(f"   ❌ Create failed: {response.status_code}")
        print(response.text)

def test_auto_sync(token):
    """Test Auto-Sync Video Statistics"""
    print("\n" + "="*50)
    print("🔄 Testing Auto-Sync Video Statistics")
    print("="*50)
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("\n1. Running auto-sync...")
    response = requests.post(
        f'{BASE_URL}/video-statistics/auto-sync',
        json={},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Auto-sync completed!")
        print(f"      Created: {data.get('created', 0)}")
        print(f"      Updated: {data.get('updated', 0)}")
        print(f"      Total: {data.get('total', 0)}")
    else:
        print(f"   ❌ Auto-sync failed: {response.status_code}")
        print(response.text)

def test_member_summary(token):
    """Test Member Daily Summary API"""
    print("\n" + "="*50)
    print("📈 Testing Member Daily Summary API")
    print("="*50)
    
    headers = {'Authorization': f'Bearer {token}'}
    today = date.today().isoformat()
    
    print("\n1. Getting member summary...")
    response = requests.get(
        f'{BASE_URL}/member-daily-summary?date={today}',
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        summaries = data.get('summaries', [])
        print(f"   ✅ Found {len(summaries)} summary record(s)")
        
        if summaries:
            for s in summaries[:3]:  # Show first 3
                print(f"      - {s.get('user_name')}: Komisi={s.get('total_commission')}, Videos={s.get('total_videos')}, Akun={s.get('total_akun')}")
    else:
        print(f"   ❌ Get failed: {response.status_code}")
        print(response.text)

def main():
    """Run all tests"""
    print("🧪 Daily Tracking API Test Suite")
    print("="*50)
    
    # Login
    token = login()
    if not token:
        print("\n❌ Cannot proceed without token")
        return
    
    try:
        # Test Daily Commissions
        test_daily_commissions(token)
        
        # Test Video Statistics
        test_video_statistics(token)
        
        # Test Auto-Sync
        test_auto_sync(token)
        
        # Test Member Summary
        test_member_summary(token)
        
        print("\n" + "="*50)
        print("✅ All tests completed!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

