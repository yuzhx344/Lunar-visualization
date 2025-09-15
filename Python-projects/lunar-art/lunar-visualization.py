import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches
from datetime import datetime, timedelta
import math

class LunarArtVisualization:
    def __init__(self, days=365):
        self.days = days
        self.lunar_data = None
        self.fig, self.ax = plt.subplots(figsize=(12, 12), facecolor='black')
        self.ax.set_facecolor('black')
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.axis('off')
        
        # 创建自定义颜色映射
        self.cmap = self.create_lunar_colormap()
        
    def create_lunar_colormap(self):
        """创建月相主题的颜色映射"""
        colors = ['#000000', '#0a0a2a', '#142b4d', '#1d4d70', 
                 '#2d6e92', '#4590b3', '#65b3d4', '#8cd5f5', 
                 '#baf6ff', '#ffffff', '#fffacd', '#ffe4b5']
        return LinearSegmentedColormap.from_list('lunar_cmap', colors, N=100)
    
    def calculate_lunar_phase(self, date):
        """计算给定日期的月相(0-1)"""
        # 使用简化算法计算月相
        days_in_lunar_cycle = 29.53
        known_new_moon = datetime(2023, 1, 21)  # 已知的新月日期
        days_since_new_moon = (date - known_new_moon).days % days_in_lunar_cycle
        phase = days_since_new_moon / days_in_lunar_cycle
        return phase
    
    def generate_lunar_data(self):
        """生成月相数据"""
        print("生成月相数据...")
        
        dates = [datetime.now() - timedelta(days=i) for i in range(self.days)]
        dates.reverse()
        
        phases = [self.calculate_lunar_phase(date) for date in dates]
        
        # 创建DataFrame
        self.lunar_data = {
            'date': dates,
            'phase': phases
        }
        
        print(f"已生成 {len(self.lunar_data['date'])} 天的数据")
        
    def calculate_moon_color(self, phase):
        """根据月相计算颜色"""
        # 月相影响色调 (0-1)
        hue = phase
        
        # 根据月相调整饱和度和亮度
        if phase < 0.25:  # 新月到上弦月
            saturation = 0.3 + 0.7 * (phase / 0.25)
            brightness = 0.2 + 0.5 * (phase / 0.25)
        elif phase < 0.5:  # 上弦月到满月
            saturation = 1.0 - 0.3 * ((phase - 0.25) / 0.25)
            brightness = 0.7 + 0.3 * ((phase - 0.25) / 0.25)
        elif phase < 0.75:  # 满月到下弦月
            saturation = 0.7 - 0.4 * ((phase - 0.5) / 0.25)
            brightness = 1.0 - 0.3 * ((phase - 0.5) / 0.25)
        else:  # 下弦月到新月
            saturation = 0.3 - 0.3 * ((phase - 0.75) / 0.25)
            brightness = 0.7 - 0.7 * ((phase - 0.75) / 0.25)
        
        return hue, saturation, brightness
    
    def draw_lunar_circle(self, day_index):
        """绘制代表一天月相的圆环"""
        phase = self.lunar_data['phase'][day_index]
        date = self.lunar_data['date'][day_index]
        
        # 计算颜色
        hue, saturation, brightness = self.calculate_moon_color(phase)
        
        # 将HSV转换为RGB
        rgb_color = self.cmap(hue)[:3]  # 获取RGB值
        # 调整饱和度和亮度
        rgb_color = tuple(c * saturation * brightness for c in rgb_color)
        
        # 计算圆环的半径
        radius = 0.9 * (day_index + 1) / self.days
        
        # 绘制圆环
        circle = patches.Circle((0, 0), radius, fill=False, 
                               color=rgb_color, linewidth=2, alpha=0.8)
        self.ax.add_patch(circle)
        
        # 添加月相标记
        if day_index % 30 == 0:  # 每30天添加一个月相标记
            # 计算月相形状
            moon_radius = radius * 0.05
            angle = np.random.uniform(0, 2*np.pi)  # 随机角度
            
            # 根据月相绘制不同形状
            if phase < 0.1 or phase > 0.9:  # 新月
                # 绘制小点表示新月
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                self.ax.plot(x, y, 'o', color=rgb_color, markersize=3, alpha=0.7)
            elif phase < 0.4:  # 娥眉月到上弦月
                # 绘制月牙
                self.draw_crescent_moon(radius, angle, phase, rgb_color)
            elif phase < 0.6:  # 满月
                # 绘制小圆表示满月
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                self.ax.plot(x, y, 'o', color=rgb_color, markersize=5, alpha=0.7)
            else:  # 下弦月到残月
                # 绘制月牙
                self.draw_crescent_moon(radius, angle, phase, rgb_color)
    
    def draw_crescent_moon(self, radius, angle, phase, color):
        """绘制月牙形状"""
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        
        # 根据月相确定月牙方向
        if phase < 0.5:
            # 娥眉月到上弦月（向右开口）
            start_angle = 30
            end_angle = 330
        else:
            # 下弦月到残月（向左开口）
            start_angle = 150
            end_angle = 450
        
        # 绘制月牙弧线
        arc = patches.Arc((x, y), 0.1, 0.1, angle=0, 
                         theta1=start_angle, theta2=end_angle, 
                         color=color, linewidth=2, alpha=0.7)
        self.ax.add_patch(arc)
    
    def create_visualization(self):
        """创建静态可视化"""
        print("创建可视化...")
        
        # 绘制中心点（代表地球）
        self.ax.plot(0, 0, 'o', color='white', markersize=8, alpha=0.8)
        
        # 绘制所有圆环
        for i in range(self.days):
            self.draw_lunar_circle(i)
        
        # 添加标题
        title = f"月相艺术可视化\n{self.days}天月相数据"
        self.fig.suptitle(title, color='white', fontsize=20, y=0.95)
        
        # 添加图例说明
        legend_text = (
            "颜色表示月相周期\n"
            "亮度表示月相明暗\n"
            "圆环半径表示时间流逝"
        )
        self.fig.text(0.05, 0.05, legend_text, color='white', fontsize=12)
        
        plt.tight_layout()
        
    def animate(self, frame):
        """动画函数"""
        if frame == 0:
            self.ax.clear()
            self.ax.set_facecolor('black')
            self.ax.set_xlim(-1.2, 1.2)
            self.ax.set_ylim(-1.2, 1.2)
            self.ax.axis('off')
            self.ax.plot(0, 0, 'o', color='white', markersize=8, alpha=0.8)
        
        if frame < self.days:
            self.draw_lunar_circle(frame)
        
        # 更新标题显示进度
        progress = min(frame / self.days, 1.0)
        self.fig.suptitle(f"月相艺术可视化 - {progress*100:.1f}%", 
                         color='white', fontsize=16, y=0.95)
        
        return []
    
    def create_animation(self):
        """创建动画"""
        print("创建动画...")
        self.fig, self.ax = plt.subplots(figsize=(10, 10), facecolor='black')
        self.ax.set_facecolor('black')
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.axis('off')
        
        ani = FuncAnimation(self.fig, self.animate, frames=self.days+1, 
                           interval=20, blit=True, repeat=False)
        
        return ani

# 主程序
if __name__ == "__main__":
    # 创建可视化实例
    lunar_art = LunarArtVisualization(days=365)
    
    # 生成月相数据
    lunar_art.generate_lunar_data()
    
    # 创建静态可视化
    plt.figure(1, figsize=(12, 12))
    lunar_art.create_visualization()
    
    # 保存静态图像
    plt.savefig('lunar_art_static.png', dpi=300, facecolor='black', bbox_inches='tight')
    print("静态图像已保存: lunar_art_static.png")
    
    # 创建动画
    plt.figure(2, figsize=(10, 10))
    ani = lunar_art.create_animation()
    
    # 保存动画
    ani.save('lunar_art_animation.gif', writer='pillow', fps=30, dpi=100)
    print("动画已保存: lunar_art_animation.gif")
    
    # 显示结果
    plt.show()