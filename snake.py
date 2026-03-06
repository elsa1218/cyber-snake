#!/usr/bin/env python3
"""
🐍 赛博贪吃蛇 - Cyber Snake
独特审美：赛博朋克霓虹 + 表情包风格
"""

import pygame
import random
import sys

# 🎨 赛博朋克配色方案
COLORS = {
    'bg': (10, 10, 30),           # 深空蓝黑背景
    'snake_head': (0, 255, 255),   # 青色蛇头
    'snake_body': (0, 128, 128),   # 深蓝绿蛇身
    'food': (255, 0, 128),         # 霓虹粉食物
    'grid': (30, 30, 60),          # 网格线
    'text': (0, 255, 255),         # 青色文字
    'glow': (255, 100, 200),       # 发光效果
}

# 🎮 游戏配置
CONFIG = {
    'width': 800,
    'height': 600,
    'cell_size': 20,
    'fps': 10,
}

class CyberSnake:
    """赛博贪吃蛇主类"""
    
    def __init__(self):
        pygame.init()
        self.config = CONFIG
        self.screen = pygame.display.set_mode(
            (self.config['width'], self.config['height'])
        )
        pygame.display.set_caption('🐍 赛博贪吃蛇 | Cyber Snake')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
    
    def reset_game(self):
        """重置游戏状态"""
        # 蛇初始位置（屏幕中央）
        center_x = self.config['width'] // (2 * self.config['cell_size'])
        center_y = self.config['height'] // (2 * self.config['cell_size'])
        self.snake = [(center_x, center_y)]
        self.direction = (1, 0)  # 初始向右
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.level = 1
    
    def spawn_food(self):
        """生成食物位置"""
        grid_w = self.config['width'] // self.config['cell_size']
        grid_h = self.config['height'] // self.config['cell_size']
        while True:
            pos = (random.randint(0, grid_w - 1), random.randint(0, grid_h - 1))
            if pos not in self.snake:
                return pos
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
        return True
    
    def handle_keydown(self, key):
        """处理按键"""
        # 防止直接反向
        if key == pygame.K_UP and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == pygame.K_DOWN and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == pygame.K_LEFT and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == pygame.K_RIGHT and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif key == pygame.K_r and self.game_over:
            self.reset_game()
        elif key == pygame.K_ESCAPE:
            sys.exit()
    
    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return
        
        # 移动蛇
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # 检测碰撞
        if self.check_collision(new_head):
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # 检测吃食物
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            # 每 50 分升级
            if self.score % 50 == 0:
                self.level += 1
                self.config['fps'] = min(20, 10 + self.level)
        else:
            self.snake.pop()
    
    def check_collision(self, pos):
        """检测碰撞"""
        grid_w = self.config['width'] // self.config['cell_size']
        grid_h = self.config['height'] // self.config['cell_size']
        
        # 撞墙
        if pos[0] < 0 or pos[0] >= grid_w:
            return True
        if pos[1] < 0 or pos[1] >= grid_h:
            return True
        
        # 撞自己
        if pos in self.snake:
            return True
        
        return False
    
    def draw(self):
        """绘制画面"""
        self.screen.fill(COLORS['bg'])
        
        # 绘制网格
        self.draw_grid()
        
        # 绘制蛇
        self.draw_snake()
        
        # 绘制食物
        self.draw_food()
        
        # 绘制 UI
        self.draw_ui()
        
        # 游戏结束画面
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_grid(self):
        """绘制赛博网格"""
        for x in range(0, self.config['width'], self.config['cell_size']):
            pygame.draw.line(self.screen, COLORS['grid'], 
                           (x, 0), (x, self.config['height']))
        for y in range(0, self.config['height'], self.config['cell_size']):
            pygame.draw.line(self.screen, COLORS['grid'],
                           (0, y), (self.config['width'], y))
    
    def draw_snake(self):
        """绘制蛇（带发光效果）"""
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(
                x * self.config['cell_size'] + 1,
                y * self.config['cell_size'] + 1,
                self.config['cell_size'] - 2,
                self.config['cell_size'] - 2
            )
            color = COLORS['snake_head'] if i == 0 else COLORS['snake_body']
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            
            # 蛇头画眼睛
            if i == 0:
                self.draw_eyes(x, y)
    
    def draw_eyes(self, x, y):
        """绘制蛇头眼睛"""
        cell = self.config['cell_size']
        eye_offset = cell // 4
        eye_size = 4
        
        # 根据方向调整眼睛位置
        dir_x, dir_y = self.direction
        if dir_x == 1:  # 向右
            eye1 = (x * cell + cell - 6, y * cell + eye_offset)
            eye2 = (x * cell + cell - 6, y * cell + cell - eye_offset - 4)
        elif dir_x == -1:  # 向左
            eye1 = (x * cell + 2, y * cell + eye_offset)
            eye2 = (x * cell + 2, y * cell + cell - eye_offset - 4)
        elif dir_y == -1:  # 向上
            eye1 = (x * cell + eye_offset, y * cell + 2)
            eye2 = (x * cell + cell - eye_offset - 4, y * cell + 2)
        else:  # 向下
            eye1 = (x * cell + eye_offset, y * cell + cell - 6)
            eye2 = (x * cell + cell - eye_offset - 4, y * cell + cell - 6)
        
        pygame.draw.circle(self.screen, (255, 255, 255), eye1, eye_size)
        pygame.draw.circle(self.screen, (255, 255, 255), eye2, eye_size)
    
    def draw_food(self):
        """绘制食物（霓虹球）"""
        x, y = self.food
        center = (
            x * self.config['cell_size'] + self.config['cell_size'] // 2,
            y * self.config['cell_size'] + self.config['cell_size'] // 2
        )
        radius = self.config['cell_size'] // 2 - 2
        
        # 外发光
        pygame.draw.circle(self.screen, COLORS['glow'], center, radius + 2)
        # 内球
        pygame.draw.circle(self.screen, COLORS['food'], center, radius)
    
    def draw_ui(self):
        """绘制 UI"""
        score_text = self.font.render(f'🏆 Score: {self.score}', True, COLORS['text'])
        level_text = self.font.render(f'⚡ Level: {self.level}', True, COLORS['text'])
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 45))
        
        # 控制提示
        hint = self.font.render('↑↓←→ 移动 | R 重来 | ESC 退出', True, (100, 100, 150))
        self.screen.blit(hint, (10, self.config['height'] - 40))
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        overlay = pygame.Surface((self.config['width'], self.config['height']))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        go_font = pygame.font.Font(None, 72)
        go_text = go_font.render('💀 GAME OVER', True, COLORS['food'])
        go_rect = go_text.get_rect(center=(self.config['width']//2, self.config['height']//2 - 50))
        self.screen.blit(go_text, go_rect)
        
        # 分数
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f'Final Score: {self.score}', True, COLORS['text'])
        score_rect = score_text.get_rect(center=(self.config['width']//2, self.config['height']//2 + 10))
        self.screen.blit(score_text, score_rect)
        
        # 重来提示
        restart_text = self.font.render('按 R 重新开始', True, COLORS['snake_head'])
        restart_rect = restart_text.get_rect(center=(self.config['width']//2, self.config['height']//2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.config['fps'])
        
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = CyberSnake()
    game.run()
