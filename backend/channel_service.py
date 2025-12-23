"""
Channel Service
Handle posting produk ke Telegram Channel
"""

import os
from models import db, Product
from telegram import Bot
import logging

logger = logging.getLogger(__name__)

class ChannelService:
    def __init__(self, bot_token: str, channel_id: str):
        """Initialize channel service"""
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.bot = Bot(token=bot_token) if bot_token else None
    
    async def post_products_summary(self):
        """Post summary of all active products to channel"""
        if not self.bot:
            logger.warning("Bot not initialized, cannot post to channel")
            return False
        
        try:
            # Get all active products
            products = Product.query.filter_by(status='active').order_by(Product.created_at.desc()).all()
            
            if not products:
                message = "📦 **Daftar Produk**\n\nTidak ada produk aktif saat ini."
            else:
                message = "📦 **DAFTAR PRODUK TERBARU**\n\n"
                message += "=" * 40 + "\n\n"
                
                for idx, product in enumerate(products, 1):
                    message += f"**{idx}. {product.product_name}**\n"
                    message += f"💰 Harga: Rp {product.product_price:,.0f}\n"
                    message += f"🔗 Link: {product.product_link}\n"
                    message += f"💵 Komisi Reguler: Rp {product.regular_commission:,.0f}\n"
                    message += f"🎯 Komisi GMV: Rp {product.gmv_max_commission:,.0f}\n"
                    if product.target_gmv > 0:
                        message += f"📊 Target GMV: Rp {product.target_gmv:,.0f}\n"
                    message += f"✅ Status: {product.status.title()}\n"
                    message += "\n" + "-" * 40 + "\n\n"
            
            # Post to channel
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Posted {len(products)} products to channel")
            return True
        
        except Exception as e:
            logger.error(f"Error posting to channel: {e}")
            return False
    
    async def post_product_update(self, product: Product, action: str = 'update'):
        """Post single product update to channel"""
        if not self.bot:
            return False
        
        try:
            if action == 'new':
                message = f"🆕 **PRODUK BARU**\n\n"
            elif action == 'update':
                message = f"🔄 **PRODUK DIUPDATE**\n\n"
            else:
                message = f"📦 **PRODUK**\n\n"
            
            message += f"**{product.product_name}**\n"
            message += f"💰 Harga: Rp {product.product_price:,.0f}\n"
            message += f"🔗 Link: {product.product_link}\n"
            message += f"💵 Komisi Reguler: Rp {product.regular_commission:,.0f}\n"
            message += f"🎯 Komisi GMV: Rp {product.gmv_max_commission:,.0f}\n"
            if product.target_gmv > 0:
                message += f"📊 Target GMV: Rp {product.target_gmv:,.0f}\n"
            message += f"✅ Status: {product.status.title()}\n"
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Posted product update to channel: {product.product_name}")
            return True
        
        except Exception as e:
            logger.error(f"Error posting product update: {e}")
            return False

