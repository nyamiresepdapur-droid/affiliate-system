"""
Notification Service
Handle creation, reading, and management of user notifications
"""
from models import db, Notification, User
from datetime import datetime, timezone
import json
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Service untuk manage notifications"""
    
    @staticmethod
    def create_notification(user_id, type, title, message=None, data=None):
        """
        Create new notification
        
        Args:
            user_id: User ID yang akan menerima notification
            type: Type notification ('report_approved', 'report_rejected', 'commission_added', 'milestone', 'reminder')
            title: Title notification
            message: Message notification (optional)
            data: Additional data sebagai dict (akan di-serialize ke JSON)
        
        Returns:
            Notification object atau None jika error
        """
        try:
            # Validate user exists
            user = User.query.get(user_id)
            if not user:
                logger.warning(f"User {user_id} not found, cannot create notification")
                return None
            
            # Serialize data to JSON string if provided
            data_json = None
            if data:
                try:
                    data_json = json.dumps(data)
                except (TypeError, ValueError) as e:
                    logger.warning(f"Failed to serialize notification data: {e}")
                    data_json = None
            
            notification = Notification(
                user_id=user_id,
                type=type,
                title=title,
                message=message,
                data=data_json,
                is_read=False
            )
            
            db.session.add(notification)
            db.session.commit()
            
            logger.info(f"Notification created for user {user_id}: {type} - {title}")
            return notification
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating notification: {e}", exc_info=True)
            return None
    
    @staticmethod
    def get_user_notifications(user_id, page=1, per_page=20, unread_only=False):
        """
        Get notifications for user dengan pagination
        
        Args:
            user_id: User ID
            page: Page number (default: 1)
            per_page: Items per page (default: 20)
            unread_only: Only get unread notifications (default: False)
        
        Returns:
            Tuple: (notifications list, pagination info)
        """
        try:
            query = Notification.query.filter_by(user_id=user_id)
            
            if unread_only:
                query = query.filter_by(is_read=False)
            
            query = query.order_by(Notification.created_at.desc())
            
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            notifications = pagination.items
            
            # Parse data JSON
            notifications_list = []
            for notif in notifications:
                notif_data = None
                if notif.data:
                    try:
                        notif_data = json.loads(notif.data)
                    except (TypeError, ValueError):
                        notif_data = None
                
                notifications_list.append({
                    'id': notif.id,
                    'type': notif.type,
                    'title': notif.title,
                    'message': notif.message,
                    'data': notif_data,
                    'is_read': notif.is_read,
                    'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S') if notif.created_at else None
                })
            
            return notifications_list, {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
            
        except Exception as e:
            logger.error(f"Error getting notifications: {e}", exc_info=True)
            return [], {}
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for user"""
        try:
            count = Notification.query.filter_by(user_id=user_id, is_read=False).count()
            return count
        except Exception as e:
            logger.error(f"Error getting unread count: {e}", exc_info=True)
            return 0
    
    @staticmethod
    def mark_as_read(notification_id, user_id=None):
        """
        Mark notification as read
        
        Args:
            notification_id: Notification ID
            user_id: Optional user_id untuk verify ownership
        
        Returns:
            True if success, False otherwise
        """
        try:
            notification = Notification.query.get(notification_id)
            if not notification:
                return False
            
            # Verify ownership if user_id provided
            if user_id and notification.user_id != user_id:
                logger.warning(f"User {user_id} tried to mark notification {notification_id} as read (owned by {notification.user_id})")
                return False
            
            notification.is_read = True
            db.session.commit()
            
            logger.info(f"Notification {notification_id} marked as read")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error marking notification as read: {e}", exc_info=True)
            return False
    
    @staticmethod
    def mark_all_as_read(user_id):
        """Mark all notifications as read for user"""
        try:
            updated = Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
            db.session.commit()
            
            logger.info(f"Marked {updated} notifications as read for user {user_id}")
            return updated
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error marking all notifications as read: {e}", exc_info=True)
            return 0
    
    @staticmethod
    def delete_notification(notification_id, user_id=None):
        """
        Delete notification
        
        Args:
            notification_id: Notification ID
            user_id: Optional user_id untuk verify ownership
        
        Returns:
            True if success, False otherwise
        """
        try:
            notification = Notification.query.get(notification_id)
            if not notification:
                return False
            
            # Verify ownership if user_id provided
            if user_id and notification.user_id != user_id:
                logger.warning(f"User {user_id} tried to delete notification {notification_id} (owned by {notification.user_id})")
                return False
            
            db.session.delete(notification)
            db.session.commit()
            
            logger.info(f"Notification {notification_id} deleted")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting notification: {e}", exc_info=True)
            return False

# Convenience functions
def create_notification(user_id, type, title, message=None, data=None):
    """Convenience function untuk create notification"""
    return NotificationService.create_notification(user_id, type, title, message, data)

