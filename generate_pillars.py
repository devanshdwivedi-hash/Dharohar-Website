import os

os.makedirs('website/assets/ui', exist_ok=True)

def generate_pillar_svg(filename, is_left=True):
    # Width: 56px, Height: 1000px
    # Palette: Nalanda Sandstone & Gold
    # Highlights: #fef08a, #fbbf24
    # Sandstone mid: #d97706, #b45309
    # Terracotta shadow: #78350f, #451a03
    # Dark stone contour: #121822, #080c10
    
    # Capital extends horizontally towards the center to meet the beam
    # Left pillar bracket extends towards X=56, right pillar bracket extends towards X=0
    
    elements = []
    
    # ── 1. Shaft (Main Vertical Body from Y=76 to Y=920) ──
    # Base fill
    elements.append('<rect x="10" y="76" width="36" height="844" fill="#0c1219"/>')
    # Fluted vertical grooves
    elements.append('<rect x="12" y="76" width="4" height="844" fill="#fbbf24" opacity="0.85"/>') # Gold highlight groove
    elements.append('<rect x="18" y="76" width="6" height="844" fill="#d97706"/>')
    elements.append('<rect x="26" y="76" width="8" height="844" fill="#b45309"/>')
    elements.append('<rect x="36" y="76" width="6" height="844" fill="#78350f"/>')
    elements.append('<rect x="44" y="76" width="2" height="844" fill="#451a03"/>')
    
    # Outer pillar borders
    elements.append('<line x1="10" y1="76" x2="10" y2="920" stroke="#f59e0b" stroke-width="2"/>')
    elements.append('<line x1="46" y1="76" x2="46" y2="920" stroke="#f59e0b" stroke-width="2"/>')

    # Decorative Ringed Bands (Patta / Mouldings) along the shaft at regular intervals
    for y_pos in [200, 350, 500, 650, 800]:
        # Stepped band
        elements.append(f'<rect x="6" y="{y_pos-8}" width="44" height="16" fill="#141d28" stroke="#d97706" stroke-width="2"/>')
        elements.append(f'<rect x="4" y="{y_pos-4}" width="48" height="8" fill="#d97706"/>')
        elements.append(f'<rect x="8" y="{y_pos-2}" width="40" height="4" fill="#fbbf24"/>')
        # Center carved diamond gem
        elements.append(f'<polygon points="28,{y_pos-6} 33,{y_pos} 28,{y_pos+6} 23,{y_pos}" fill="#fef08a"/>')

    # ── 2. Stepped Capital (Top: Y=0 to Y=76) ──
    # The capital flares outward to support the horizontal Torana beam
    if is_left:
        # Left pillar: Bracket flares rightwards into the beam
        # Upper abacus / beam support ledge
        elements.append('<polygon points="0,0 56,0 56,22 46,38 46,76 10,76 10,38 0,22" fill="#141d28" stroke="#f59e0b" stroke-width="2"/>')
        # Inner decorative steps
        elements.append('<rect x="2" y="4" width="52" height="6" fill="#fef08a"/>')
        elements.append('<rect x="4" y="12" width="50" height="8" fill="#d97706"/>')
        elements.append('<rect x="8" y="24" width="40" height="10" fill="#b45309"/>')
        elements.append('<rect x="12" y="38" width="32" height="12" fill="#1b2533"/>')
        # Lotus rosette on capital
        elements.append('<circle cx="28" cy="56" r="8" fill="#d97706" stroke="#fbbf24" stroke-width="2"/>')
        elements.append('<circle cx="28" cy="56" r="4" fill="#fef08a"/>')
        # Supporting corbel bracket extending rightward to lock with beam
        elements.append('<polygon points="46,16 56,8 56,28 46,36" fill="#fbbf24"/>')
    else:
        # Right pillar: Bracket flares leftwards into the beam
        elements.append('<polygon points="0,0 56,0 56,22 46,38 46,76 10,76 10,38 0,22" fill="#141d28" stroke="#f59e0b" stroke-width="2"/>')
        elements.append('<rect x="2" y="4" width="52" height="6" fill="#fef08a"/>')
        elements.append('<rect x="2" y="12" width="50" height="8" fill="#d97706"/>')
        elements.append('<rect x="8" y="24" width="40" height="10" fill="#b45309"/>')
        elements.append('<rect x="12" y="38" width="32" height="12" fill="#1b2533"/>')
        elements.append('<circle cx="28" cy="56" r="8" fill="#d97706" stroke="#fbbf24" stroke-width="2"/>')
        elements.append('<circle cx="28" cy="56" r="4" fill="#fef08a"/>')
        # Supporting corbel bracket extending leftward to lock with beam
        elements.append('<polygon points="10,16 0,8 0,28 10,36" fill="#fbbf24"/>')

    # ── 3. Stepped Base Plinth (Bottom: Y=920 to Y=1000) ──
    # Wide stepped stone pedestal
    elements.append('<rect x="8" y="920" width="40" height="16" fill="#141d28" stroke="#d97706" stroke-width="2"/>')
    elements.append('<rect x="12" y="924" width="32" height="8" fill="#d97706"/>')
    elements.append('<rect x="4" y="936" width="48" height="20" fill="#141d28" stroke="#f59e0b" stroke-width="2"/>')
    elements.append('<rect x="8" y="942" width="40" height="8" fill="#b45309"/>')
    elements.append('<rect x="0" y="956" width="56" height="44" fill="#090e15" stroke="#f59e0b" stroke-width="2"/>')
    elements.append('<rect x="4" y="962" width="48" height="12" fill="#d97706"/>')
    elements.append('<rect x="8" y="976" width="40" height="6" fill="#fbbf24"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 1000" width="100%" height="100%" preserveAspectRatio="none" style="shape-rendering: crispEdges;">
{''.join(elements)}
</svg>'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'Generated {filename}')

generate_pillar_svg('website/assets/ui/pillar_left.svg', is_left=True)
generate_pillar_svg('website/assets/ui/pillar_right.svg', is_left=False)

# ── 4. Torana Beam Frieze (Horizontal Ornamental Accent) ──
frieze = []
frieze.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 16" width="100%" height="100%" preserveAspectRatio="none">')
# Repeating dentil / stepped tooth frieze
for x in range(0, 400, 20):
    frieze.append(f'<rect x="{x+2}" y="2" width="12" height="8" fill="#fbbf24" stroke="#78350f" stroke-width="1"/>')
    frieze.append(f'<circle cx="{x+8}" cy="13" r="1.5" fill="#fef08a"/>')
frieze.append('</svg>')

with open('website/assets/ui/beam_frieze.svg', 'w', encoding='utf-8') as f:
    f.write(''.join(frieze))
print('Generated website/assets/ui/beam_frieze.svg')
