import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── 1. Zepto Sales Dashboard ──────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 9), facecolor='#fce4f0')
fig.patch.set_facecolor('#fce4f0')

# Title bar
ax_title = fig.add_axes([0, 0.88, 1, 0.12], facecolor='#e8b4d0')
ax_title.set_xlim(0, 1); ax_title.set_ylim(0, 1); ax_title.axis('off')
ax_title.text(0.18, 0.55, 'zepto', fontsize=28, fontweight='bold', color='#8B008B',
              fontfamily='DejaVu Sans', va='center', style='italic')
ax_title.text(0.5, 0.55, 'Zepto Sales in a Month', fontsize=22, fontweight='bold',
              color='#8B008B', va='center', ha='center')

# KPI boxes
for i, (val, lbl) in enumerate([('6M', 'Revenue Collection'), ('9,386', 'Sales by Category')]):
    ax = fig.add_axes([0.02 + i*0.25, 0.68, 0.22, 0.18], facecolor='#fce4f0')
    ax.axis('off')
    ax.text(0.5, 0.7, val, fontsize=26, fontweight='bold', ha='center', va='center', color='#222')
    ax.text(0.5, 0.2, lbl, fontsize=9, ha='center', va='center', color='#c060a0')

# Bar chart - Revenue by Product
ax1 = fig.add_axes([0.02, 0.35, 0.28, 0.30], facecolor='#fce4f0')
products = ['Coca Cola', 'Maggi', 'Parle-G', 'Nestle', 'Amul', 'Oreo', 'Britannia']
vals = [95, 92, 88, 85, 82, 79, 76]
bars = ax1.bar(range(len(products)), vals, color='#e88ab0', width=0.6)
ax1.set_xticks(range(len(products)))
ax1.set_xticklabels(products, rotation=45, ha='right', fontsize=7)
ax1.set_title('Sum of Total Revenue by Month', fontsize=8, color='#c060a0')
ax1.set_facecolor('#fce4f0'); ax1.spines[['top','right']].set_visible(False)
ax1.tick_params(colors='#888', labelsize=7)

# Horizontal bar - Sales by City
ax2 = fig.add_axes([0.32, 0.35, 0.30, 0.30], facecolor='#fce4f0')
cities = ['HYDERABAD', 'PUNE', 'BANGALORE', 'DELHI', 'MUMBAI', 'CHENNAI']
city_vals = [9200, 8800, 7600, 7000, 6800, 6500]
ax2.barh(cities, city_vals, color='#e88ab0', height=0.6)
ax2.set_title('Sales by Cities', fontsize=8, color='#c060a0')
ax2.set_facecolor('#fce4f0'); ax2.spines[['top','right']].set_visible(False)
ax2.tick_params(colors='#888', labelsize=7)

# Pie chart
ax3 = fig.add_axes([0.32, 0.05, 0.22, 0.28], facecolor='#fce4f0')
pie_vals = [21.59, 18.01, 17.59, 14.6, 14.44, 13.77]
pie_colors = ['#6a0dad', '#9b30ff', '#c77dff', '#e0aaff', '#ff6eb4', '#ff9ed2']
ax3.pie(pie_vals, colors=pie_colors, startangle=90,
        wedgeprops={'linewidth': 0.5, 'edgecolor': 'white'})
ax3.set_title('Sum of Original Price', fontsize=8, color='#c060a0')

# Line chart
ax4 = fig.add_axes([0.64, 0.05, 0.34, 0.28], facecolor='#fce4f0')
months = range(1, 13)
for city, color in zip(['HYDERABAD', 'PUNE', 'BANGALORE'],
                        ['#ff6eb4', '#9b30ff', '#6a0dad']):
    ax4.plot(months, np.random.randint(800, 2200, 12), color=color, linewidth=1.5, label=city)
ax4.set_title('Sum of Current Price', fontsize=8, color='#c060a0')
ax4.set_facecolor('#fce4f0'); ax4.spines[['top','right']].set_visible(False)
ax4.tick_params(colors='#888', labelsize=7)
ax4.legend(fontsize=6, framealpha=0)

# Waterfall-style bar
ax5 = fig.add_axes([0.02, 0.05, 0.28, 0.28], facecolor='#fce4f0')
cats = ['Snacks', 'Beverages', 'Grocery', 'Instant\nFood', 'Confect.', 'Dairy', 'Total']
inc = [8000, 15000, 20000, 25000, 28000, 30000, 32000]
colors5 = ['#90ee90']*6 + ['#4169e1']
ax5.bar(cats, inc, color=colors5, width=0.6)
ax5.set_facecolor('#fce4f0'); ax5.spines[['top','right']].set_visible(False)
ax5.tick_params(colors='#888', labelsize=7)

plt.savefig('c:/Users/HP/OneDrive/Attachments/edison_portfolio/site/zepto-dashboard.png',
            dpi=120, bbox_inches='tight', facecolor='#fce4f0')
plt.close()
print("Zepto done")

# ── 2. Agricultural Performance Dashboard ────────────────────────────────────
fig2 = plt.figure(figsize=(16, 9), facecolor='#f5f0e8')
fig2.patch.set_facecolor('#f5f0e8')

# Title
ax_t = fig2.add_axes([0, 0.88, 1, 0.12], facecolor='#e8dcc8')
ax_t.axis('off')
ax_t.text(0.5, 0.55, 'Seasonal Agricultural Performance Analysis',
          fontsize=22, fontweight='bold', color='#3d5a1e', ha='center', va='center')

# KPI strip
for i, (v, l) in enumerate([('4', 'Crops Monitored'), ('3', 'Seasons Tracked'),
                              ('12%', 'Avg Yield Increase'), ('5.6T+', 'Kharif Output')]):
    ax = fig2.add_axes([0.02 + i*0.24, 0.70, 0.20, 0.16], facecolor='#ede0c4')
    ax.axis('off')
    ax.text(0.5, 0.65, v, fontsize=24, fontweight='bold', ha='center', color='#3d5a1e')
    ax.text(0.5, 0.2, l, fontsize=8, ha='center', color='#7a6a4a')

# Grouped bar - Seasonal Crop Production
ax6 = fig2.add_axes([0.02, 0.35, 0.44, 0.32], facecolor='#f5f0e8')
crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane']
x = np.arange(len(crops)); w = 0.25
kharif = [42, 18, 35, 28, 45]
rabi   = [15, 38, 12, 8,  10]
zaid   = [8,  5,  20, 5,  30]
ax6.bar(x - w, kharif, w, label='Kharif', color='#e07b39')
ax6.bar(x,     rabi,   w, label='Rabi',   color='#4a9e6b')
ax6.bar(x + w, zaid,   w, label='Zaid',   color='#5b8dd9')
ax6.set_xticks(x); ax6.set_xticklabels(crops, fontsize=8)
ax6.set_title('Seasonal Crop Production', fontsize=9, color='#3d5a1e', fontweight='bold')
ax6.legend(fontsize=7, framealpha=0); ax6.set_facecolor('#f5f0e8')
ax6.spines[['top','right']].set_visible(False); ax6.tick_params(colors='#888', labelsize=7)

# Line chart - Yield Trend
ax7 = fig2.add_axes([0.02, 0.05, 0.44, 0.27], facecolor='#f5f0e8')
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for crop, color, vals in [
    ('Rice',  '#e07b39', [20,22,25,28,32,38,42,40,35,30,25,22]),
    ('Wheat', '#4a9e6b', [35,38,40,38,32,25,18,15,18,25,32,36]),
    ('Maize', '#5b8dd9', [15,18,22,28,35,38,35,30,25,20,16,14])]:
    ax7.plot(months, vals, color=color, linewidth=2, label=crop, marker='o', markersize=3)
ax7.set_title('Yield Trend', fontsize=9, color='#3d5a1e', fontweight='bold')
ax7.legend(fontsize=7, framealpha=0); ax7.set_facecolor('#f5f0e8')
ax7.spines[['top','right']].set_visible(False); ax7.tick_params(colors='#888', labelsize=7)
ax7.set_xticklabels(months, rotation=45, ha='right', fontsize=6)

# Horizontal bar - Crop Performance %
ax8 = fig2.add_axes([0.52, 0.35, 0.44, 0.32], facecolor='#f5f0e8')
perf_crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane']
perf_vals  = [92, 78, 65, 55, 88]
colors8 = ['#e07b39','#4a9e6b','#5b8dd9','#c0392b','#8e44ad']
bars8 = ax8.barh(perf_crops, perf_vals, color=colors8, height=0.5)
for bar, val in zip(bars8, perf_vals):
    ax8.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val}%',
             va='center', fontsize=8, color='#444')
ax8.set_xlim(0, 110)
ax8.set_title('Crop Performance', fontsize=9, color='#3d5a1e', fontweight='bold')
ax8.set_facecolor('#f5f0e8'); ax8.spines[['top','right']].set_visible(False)
ax8.tick_params(colors='#888', labelsize=8)

# Revenue comparison bar
ax9 = fig2.add_axes([0.52, 0.05, 0.44, 0.27], facecolor='#f5f0e8')
seasons = ['Kharif', 'Rabi', 'Zaid']
revenue = [700000, 420000, 280000]
profit  = [490000, 260000, 150000]
x9 = np.arange(3); w9 = 0.35
ax9.bar(x9 - w9/2, revenue, w9, label='Revenue (₹)', color='#e07b39', alpha=0.85)
ax9.bar(x9 + w9/2, profit,  w9, label='Profit (₹)',  color='#4a9e6b', alpha=0.85)
ax9.set_xticks(x9); ax9.set_xticklabels(seasons, fontsize=9)
ax9.set_title('Revenue vs Profit by Season', fontsize=9, color='#3d5a1e', fontweight='bold')
ax9.legend(fontsize=7, framealpha=0); ax9.set_facecolor('#f5f0e8')
ax9.spines[['top','right']].set_visible(False); ax9.tick_params(colors='#888', labelsize=7)
ax9.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1e5:.0f}L'))

plt.savefig('c:/Users/HP/OneDrive/Attachments/edison_portfolio/site/agri-dashboard.png',
            dpi=120, bbox_inches='tight', facecolor='#f5f0e8')
plt.close()
print("Agri done")
