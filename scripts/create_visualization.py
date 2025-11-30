#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

# Data from our fault injection campaign
categories = ['No Effect\n(Golden Tag)', 'Program\nCrashes', 'Corrupted Tags\n(Exploitable)']
values = [5682, 37837, 3481]
colors = ['#2ecc71', '#e74c3c', '#f39c12']
percentages = [12.0, 80.5, 7.4]

# Create pie chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
wedges, texts, autotexts = ax1.pie(values, labels=categories, colors=colors, 
                                     autopct='%1.1f%%', startangle=90,
                                     textprops={'fontsize': 12, 'weight': 'bold'})
ax1.set_title('AES-GCM Fault Injection Results\n(5,000 faults injected into GHASH)', 
              fontsize=14, weight='bold', pad=20)

# Bar chart
bars = ax2.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Number of Faults', fontsize=12, weight='bold')
ax2.set_title('Fault Injection Outcomes', fontsize=14, weight='bold')
ax2.set_ylim(0, max(values) * 1.1)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=11, weight='bold')

plt.tight_layout()
plt.savefig('aes_gcm_fault_results.png', dpi=300, bbox_inches='tight')
print("✓ Saved visualization to: aes_gcm_fault_results.png")

# Create a detailed breakdown chart
fig2, ax3 = plt.subplots(figsize=(10, 6))

exploitable_tags = {
    '0x354b2b1b': 49,
    '0xe2512ef': 41,
    '0xd4a4e780': 38,
    '0x0 (bypass)': 38,
    '0xea86c592': 37,
    '0xb0f57a71': 37,
    '0xd48171b3': 35,
    'Others': 3206
}

tags = list(exploitable_tags.keys())
counts = list(exploitable_tags.values())

bars = ax3.barh(tags, counts, color='#f39c12', edgecolor='black', linewidth=1.5)
ax3.set_xlabel('Number of Occurrences', fontsize=12, weight='bold')
ax3.set_title('Top Exploitable Tag Values\n(Authentication Bypass Candidates)', 
              fontsize=14, weight='bold')
ax3.invert_yaxis()

# Highlight the zero tag
bars[3].set_color('#e74c3c')
bars[3].set_label('Complete Bypass (tag=0)')
ax3.legend()

for i, (bar, count) in enumerate(zip(bars, counts)):
    ax3.text(count + 50, i, str(count), va='center', fontsize=10, weight='bold')

plt.tight_layout()
plt.savefig('exploitable_tags.png', dpi=300, bbox_inches='tight')
print("✓ Saved exploitable tags chart to: exploitable_tags.png")

print("\n" + "="*60)
print("VISUALIZATION COMPLETE")
print("="*60)