#!/usr/bin/env python3
"""
🐍 赛博贪吃蛇 - Cyber Snake
独特审美：赛博朋克霓虹 + 表情包风格
"""

import pygame
import random
import sys
import math
import json
import os

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

# 🎭 蛇皮肤系统（emoji 主题）
SKINS = {
    'cyber': {'head': '🤖', 'body': '■', 'color': COLORS['snake_head']},
    'classic': {'head': '🐍', 'body': '●', 'color': (0, 200, 0)},
    'rainbow': {'head': '🦄', 'body': '◆', 'color': (255, 0, 255)},
    'fire': {'head': '🔥', 'body': '▲', 'color': (255, 100, 0)},
    'ghost': {'head': '👻', 'body': '○', 'color': (200, 200, 200)},
}

# 🍎 特殊食物类型
FOOD_TYPES = {
    'normal': {'color': COLORS['food'], 'points': 10, 'effect': None, 'emoji': '🍎'},
    'double': {'color': (255, 215, 0), 'points': 20, 'effect': 'double', 'emoji': '⭐', 'duration': 10},
    'speed': {'color': (0, 255, 0), 'points': 15, 'effect': 'speed', 'emoji': '⚡', 'duration': 8},
    'slow': {'color': (0, 100, 255), 'points': 15, 'effect': 'slow', 'emoji': '🐌', 'duration': 8},
    'bonus': {'color': (255, 0, 255), 'points': 50, 'effect': 'bonus', 'emoji': '💎', 'duration': 0},
}

# 🎮 游戏配置
CONFIG = {
    'width': 800,
    'height': 600,
    'cell_size': 20,
    'fps': 6,  # 初始速度降低（6 -> 10）
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
        self.score = 0
        self.game_over = False
        self.level = 1
        self.particles = []  # 粒子效果列表
        self.show_leaderboard = False
        self.paused = False
        self.current_skin = 'cyber'
        self.active_effects = {}  # 当前激活的效果
        self.food_type = 'normal'
        self.food = self.spawn_food()
        self.load_leaderboard()
        self.init_sound()
        self.game_state = 'menu'  # menu, playing, paused, game_over
    
    def spawn_food(self):
        """生成食物位置（支持特殊食物类型）"""
        grid_w = self.config['width'] // self.config['cell_size']
        grid_h = self.config['height'] // self.config['cell_size']
        
        # 随机决定食物类型（80% 普通，20% 特殊）
        if random.random() < 0.8:
            self.food_type = 'normal'
        else:
            special_types = ['double', 'speed', 'slow', 'bonus']
            self.food_type = random.choice(special_types)
        
        while True:
            pos = (random.randint(0, grid_w - 1), random.randint(0, grid_h - 1))
            if pos not in self.snake:
                return pos
    
    def init_sound(self):
        """初始化音效系统"""
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        # 用 pygame 合成简单音效（不需要外部文件）
        self.sound_enabled = True
    
    def play_sound(self, sound_type):
        """播放音效"""
        if not self.sound_enabled:
            return
        # 简化版本：用 print 代替实际音效（避免复杂音频生成）
        # 实际项目中可以添加真实的音效文件
        pass
    
    def apply_effect(self, effect_type):
        """应用食物效果"""
        if effect_type == 'double':
            self.active_effects['double_score'] = 10
        elif effect_type == 'speed':
            self.config['fps'] = min(25, self.config['fps'] + 5)
            self.active_effects['speed'] = 8
        elif effect_type == 'slow':
            self.config['fps'] = max(5, self.config['fps'] - 3)
            self.active_effects['slow'] = 8
        elif effect_type == 'bonus':
            self.score += 100
    
    def update_effects(self):
        """更新效果计时器"""
        for effect in list(self.active_effects.keys()):
            self.active_effects[effect] -= 1
            if self.active_effects[effect] <= 0:
                if effect == 'speed' or effect == 'slow':
                    self.config['fps'] = 10 + self.level
                del self.active_effects[effect]
    
    def change_skin(self, skin_name):
        """切换蛇皮肤"""
        if skin_name in SKINS:
            self.current_skin = skin_name
    
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
        # 主菜单状态
        if self.game_state == 'menu':
            if key == pygame.K_SPACE:
                self.game_state = 'playing'
                self.reset_game()
            elif key == pygame.K_h:
                self.show_leaderboard = True
            elif key == pygame.K_ESCAPE:
                sys.exit()
            return
        
        # 排行榜显示时按任意键返回
        if self.show_leaderboard:
            self.show_leaderboard = False
            return
        
        # 暂停状态
        if self.paused:
            if key == pygame.K_p:
                self.paused = False
                self.game_state = 'playing'
            elif key == pygame.K_ESCAPE:
                sys.exit()
            return
        
        # 游戏结束状态
        if self.game_over:
            if key == pygame.K_r:
                self.reset_game()
                self.game_state = 'playing'
            elif key == pygame.K_ESCAPE:
                sys.exit()
            return
        
        # 游戏进行中
        if self.game_state == 'playing':
            # 防止直接反向
            if key == pygame.K_UP and self.direction != (0, 1):
                self.direction = (0, -1)
            elif key == pygame.K_DOWN and self.direction != (0, -1):
                self.direction = (0, 1)
            elif key == pygame.K_LEFT and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.direction = (1, 0)
            elif key == pygame.K_p:
                self.paused = True
                self.game_state = 'paused'
            elif key == pygame.K_h:
                self.show_leaderboard = True
            elif key == pygame.K_1:
                self.change_skin('cyber')
            elif key == pygame.K_2:
                self.change_skin('classic')
            elif key == pygame.K_3:
                self.change_skin('rainbow')
            elif key == pygame.K_4:
                self.change_skin('fire')
            elif key == pygame.K_5:
                self.change_skin('ghost')
            elif key == pygame.K_m:
                self.sound_enabled = not self.sound_enabled
            elif key == pygame.K_ESCAPE:
                sys.exit()
    
    def update(self):
        """更新游戏状态"""
        if self.show_leaderboard:
            self.update_particles()
            return
        
        if self.game_state == 'menu' or self.game_state == 'paused':
            return
        
        if self.game_over:
            self.game_state = 'game_over'
            self.update_particles()
            return
        
        # 移动蛇
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # 检测碰撞
        if self.check_collision(new_head):
            self.game_over = True
            self.game_state = 'game_over'
            self.save_leaderboard()
            return
        
        self.snake.insert(0, new_head)
        
        # 检测吃食物
        if new_head == self.food:
            food_data = FOOD_TYPES.get(self.food_type, FOOD_TYPES['normal'])
            points = food_data['points']
            if 'double_score' in self.active_effects:
                points *= 2
            self.score += points
            self.play_sound('eat')
            self.create_particles(new_head[0], new_head[1], food_data['color'])
            self.apply_effect(food_data['effect'])
            self.food = self.spawn_food()
            # 每 50 分升级
            if self.score % 50 == 0:
                self.level += 1
                self.config['fps'] = min(20, 10 + self.level)
        else:
            self.snake.pop()
        
        # 更新粒子和效果
        self.update_particles()
        self.update_effects()
    
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
        # 根据游戏状态绘制不同画面
        if self.game_state == 'menu':
            self.draw_menu()
        elif self.game_state == 'paused':
            # 先绘制游戏画面，再覆盖暂停层
            self.screen.fill(COLORS['bg'])
            self.draw_grid()
            self.draw_snake()
            self.draw_food()
            self.draw_particles()
            self.draw_ui()
            self.draw_pause()
        elif self.game_state == 'game_over':
            self.screen.fill(COLORS['bg'])
            self.draw_grid()
            self.draw_snake()
            self.draw_food()
            self.draw_particles()
            self.draw_ui()
            self.draw_game_over()
        else:  # playing
            self.screen.fill(COLORS['bg'])
            self.draw_grid()
            self.draw_snake()
            self.draw_food()
            self.draw_particles()
            self.draw_ui()
        
        # 排行榜覆盖层
        if self.show_leaderboard:
            self.draw_leaderboard()
        
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
        """绘制蛇（带皮肤系统）"""
        skin = SKINS.get(self.current_skin, SKINS['cyber'])
        color = skin['color']
        
        # 绘制蛇身
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(
                x * self.config['cell_size'] + 1,
                y * self.config['cell_size'] + 1,
                self.config['cell_size'] - 2,
                self.config['cell_size'] - 2
            )
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
        
        # 绘制蛇头 emoji
        head_x, head_y = self.snake[0]
        emoji_font = pygame.font.Font(None, self.config['cell_size'] * 2)
        emoji_text = emoji_font.render(skin['head'], True, color)
        emoji_rect = emoji_text.get_rect(center=(
            head_x * self.config['cell_size'] + self.config['cell_size'] // 2,
            head_y * self.config['cell_size'] + self.config['cell_size'] // 2
        ))
        self.screen.blit(emoji_text, emoji_rect)
    
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
        """绘制食物（带类型 emoji）"""
        x, y = self.food
        food_data = FOOD_TYPES.get(self.food_type, FOOD_TYPES['normal'])
        
        # 绘制外发光
        center = (
            x * self.config['cell_size'] + self.config['cell_size'] // 2,
            y * self.config['cell_size'] + self.config['cell_size'] // 2
        )
        pygame.draw.circle(self.screen, COLORS['glow'], center, 12)
        pygame.draw.circle(self.screen, food_data['color'], center, 8)
        
        # 绘制食物 emoji
        emoji_font = pygame.font.Font(None, self.config['cell_size'] * 2)
        emoji_text = emoji_font.render(food_data['emoji'], True, (255, 255, 255))
        emoji_rect = emoji_text.get_rect(center=center)
        self.screen.blit(emoji_text, emoji_rect)
    
    def draw_ui(self):
        """绘制 UI"""
        score_text = self.font.render(f'🏆 Score: {self.score}', True, COLORS['text'])
        level_text = self.font.render(f'⚡ Level: {self.level}', True, COLORS['text'])
        skin_text = self.font.render(f'🎭 Skin: {self.current_skin}', True, COLORS['glow'])
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 45))
        self.screen.blit(skin_text, (10, 80))
        
        # 显示激活的效果
        effect_y = 115
        for effect, duration in self.active_effects.items():
            effect_color = COLORS['food'] if effect == 'double_score' else (255, 255, 0)
            effect_txt = self.font.render(f'{effect}: {duration}s', True, effect_color)
            self.screen.blit(effect_txt, (10, effect_y))
            effect_y += 30
        
        # 控制提示
        hint = self.font.render('↑↓←→ 移动 | 1-5 换皮肤 | R 重来 | H 排行榜 | M 音效 | ESC 退出', True, (100, 100, 150))
        self.screen.blit(hint, (10, self.config['height'] - 40))
    
    def create_particles(self, x, y, color, count=15):
        """创建粒子爆炸效果"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            self.particles.append({
                'x': x * self.config['cell_size'] + self.config['cell_size'] // 2,
                'y': y * self.config['cell_size'] + self.config['cell_size'] // 2,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.uniform(0.5, 1.0),
                'color': color,
                'size': random.randint(2, 5)
            })
    
    def update_particles(self):
        """更新粒子状态"""
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.02
            p['size'] = max(1, p['size'] - 0.1)
        self.particles = [p for p in self.particles if p['life'] > 0]
    
    def draw_particles(self):
        """绘制粒子"""
        for p in self.particles:
            alpha = int(255 * p['life'])
            color = (*p['color'][:3], alpha)
            pygame.draw.circle(self.screen, p['color'], 
                             (int(p['x']), int(p['y'])), int(p['size']))
    
    def load_leaderboard(self):
        """加载排行榜"""
        self.leaderboard_file = os.path.join(os.path.dirname(__file__), 'leaderboard.json')
        try:
            with open(self.leaderboard_file, 'r') as f:
                self.leaderboard = json.load(f)
        except:
            self.leaderboard = []
    
    def save_leaderboard(self):
        """保存排行榜"""
        self.leaderboard.append({
            'score': self.score,
            'level': self.level,
            'date': pygame.time.get_ticks()
        })
        self.leaderboard.sort(key=lambda x: x['score'], reverse=True)
        self.leaderboard = self.leaderboard[:10]  # 保留前 10 名
        try:
            with open(self.leaderboard_file, 'w') as f:
                json.dump(self.leaderboard, f)
        except:
            pass
    
    def draw_leaderboard(self):
        """绘制排行榜"""
        overlay = pygame.Surface((self.config['width'], self.config['height']))
        overlay.set_alpha(200)
        overlay.fill((5, 5, 20))
        self.screen.blit(overlay, (0, 0))
        
        title_font = pygame.font.Font(None, 56)
        title = title_font.render('🏆 排行榜 LEADERBOARD', True, COLORS['glow'])
        self.screen.blit(title, (self.config['width']//2 - title.get_width()//2, 50))
        
        for i, entry in enumerate(self.leaderboard[:10]):
            color = COLORS['snake_head'] if i == 0 else COLORS['text']
            if i == 0:
                text = f'🥇 #{i+1} Score: {entry["score"]} Level: {entry["level"]}'
            elif i < 3:
                text = f'🥈 #{i+1} Score: {entry["score"]} Level: {entry["level"]}' if i == 1 else f'🥉 #{i+1} Score: {entry["score"]} Level: {entry["level"]}'
            else:
                text = f'#{i+1} Score: {entry["score"]} Level: {entry["level"]}'
            
            entry_text = self.font.render(text, True, color)
            self.screen.blit(entry_text, (self.config['width']//2 - entry_text.get_width()//2, 120 + i * 40))
        
        hint = self.font.render('按任意键返回', True, (100, 100, 150))
        self.screen.blit(hint, (self.config['width']//2 - hint.get_width()//2, self.config['height'] - 80))
    
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
    
    def draw_menu(self):
        """绘制主菜单"""
        # 背景渐变
        for y in range(self.config['height']):
            color_val = int(20 + 10 * math.sin(y / 50 + pygame.time.get_ticks() / 1000))
            pygame.draw.line(self.screen, (color_val, color_val, color_val + 20),
                           (0, y), (self.config['width'], y))
        
        # 游戏标题（动态颜色）
        title_font = pygame.font.Font(None, 96)
        hue = (pygame.time.get_ticks() / 20) % 360
        title_color = (int(128 + 127 * math.sin(hue / 180 * math.pi)),
                      int(128 + 127 * math.sin((hue + 120) / 180 * math.pi)),
                      int(128 + 127 * math.sin((hue + 240) / 180 * math.pi)))
        title_text = title_font.render('🐍 CYBER SNAKE', True, title_color)
        title_rect = title_text.get_rect(center=(self.config['width']//2, self.config['height']//3))
        self.screen.blit(title_text, title_rect)
        
        # 副标题
        subtitle_font = pygame.font.Font(None, 36)
        subtitle = subtitle_font.render('赛博朋克贪吃蛇', True, COLORS['text'])
        subtitle_rect = subtitle.get_rect(center=(self.config['width']//2, self.config['height']//3 + 50))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 开始按钮
        start_font = pygame.font.Font(None, 48)
        start_text = start_font.render('按 SPACE 开始游戏', True, COLORS['snake_head'])
        start_rect = start_text.get_rect(center=(self.config['width']//2, self.config['height']//2))
        self.screen.blit(start_text, start_rect)
        
        # 控制说明
        controls = [
            '↑↓←→ 移动蛇',
            '1-5 切换皮肤',
            'P 暂停',
            'H 排行榜',
            'M 音效开关',
            'ESC 退出'
        ]
        ctrl_font = pygame.font.Font(None, 28)
        for i, ctrl in enumerate(controls):
            ctrl_text = ctrl_font.render(ctrl, True, (150, 150, 200))
            ctrl_rect = ctrl_text.get_rect(center=(self.config['width']//2, self.config['height']//2 + 80 + i * 30))
            self.screen.blit(ctrl_text, ctrl_rect)
        
        # 底部提示
        hint_font = pygame.font.Font(None, 24)
        hint = hint_font.render('Press SPACE to Start | H for Leaderboard | ESC to Quit', True, (100, 100, 150))
        hint_rect = hint.get_rect(center=(self.config['width']//2, self.config['height'] - 40))
        self.screen.blit(hint, hint_rect)
    
    def draw_pause(self):
        """绘制暂停画面"""
        overlay = pygame.Surface((self.config['width'], self.config['height']))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 暂停文字
        pause_font = pygame.font.Font(None, 72)
        pause_text = pause_font.render('⏸️ PAUSED', True, COLORS['snake_head'])
        pause_rect = pause_text.get_rect(center=(self.config['width']//2, self.config['height']//2 - 30))
        self.screen.blit(pause_text, pause_rect)
        
        # 继续提示
        resume_text = self.font.render('按 P 继续游戏', True, COLORS['text'])
        resume_rect = resume_text.get_rect(center=(self.config['width']//2, self.config['height']//2 + 30))
        self.screen.blit(resume_text, resume_rect)
    
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
    game.game_state = 'menu'  # 从主菜单开始
    game.run()
