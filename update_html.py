#!/usr/bin/env python3
"""
Update index.html with new sections
"""

# Read the current HTML
with open('index.html', 'r') as f:
    html = f.read()

# Update stylesheet reference
html = html.replace('href="styles.css"', 'href="styles-new.css"')

# Update header logo
html = html.replace('<div class="logo">🤝</div>', '<div class="logo">🏡</div>')

# Find and replace navigation
nav_old_start = '<nav>'
nav_old_end = '</nav>'

nav_new = '''    <nav>
        <div class="nav-container">
            <ul class="nav-links">
                <li><a href="#home" class="nav-link active" data-section="home">🏠 Home</a></li>
                <li><a href="#mental-health" class="nav-link" data-section="mental-health">💙 Mental Health</a></li>
                <li><a href="#legal" class="nav-link" data-section="legal">⚖️ Legal Support</a></li>
                <li><a href="#community" class="nav-link" data-section="community">👥 Community</a></li>
                <li><a href="#child-health" class="nav-link" data-section="child-health">🏥 Child Health</a></li>
                <li><a href="#child-development" class="nav-link" data-section="child-development">👶 Child Development</a></li>
                <li><a href="#sports-recreation" class="nav-link" data-section="sports-recreation">⚽ Sports & Recreation</a></li>
                <li><a href="#arts-expression" class="nav-link" data-section="arts-expression">🎨 Arts & Expression</a></li>
                <li><a href="#mens-support" class="nav-link" data-section="mens-support">👨 Men's Support</a></li>
                <li><a href="#family-events" class="nav-link" data-section="family-events">🎉 Family Events</a></li>
                <li><a href="#rural-remote" class="nav-link" data-section="rural-remote">🌾 Rural & Remote</a></li>
                <li><a href="#financial" class="nav-link" data-section="financial">💰 Financial Help</a></li>
                <li><a href="#emergency" class="nav-link" data-section="emergency">🚨 Emergency</a></li>
                <li><a href="#ai-chat" class="nav-link" data-section="ai-chat">💬 AI Support Chat</a></li>
            </ul>
        </div>
    </nav>'''

# Replace navigation
start_idx = html.find(nav_old_start)
end_idx = html.find(nav_old_end) + len(nav_old_end)
if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + nav_new + html[end_idx:]

# Add new sections before the AI chat section
ai_chat_marker = '<!-- AI Chat Section -->'
ai_chat_idx = html.find(ai_chat_marker)

new_sections = '''
        <!-- Child Health Section -->
        <section id="child-health" class="section">
            <div class="section-header">
                <h2>🏥 Child Health Services</h2>
                <p>Comprehensive health services for your children from birth through adolescence. Free health checks, immunizations, and developmental support.</p>
            </div>
            <div id="child-health-resources" class="resources-grid"></div>
        </section>

        <!-- Sports & Recreation Section -->
        <section id="sports-recreation" class="section">
            <div class="section-header">
                <h2>⚽ Sports & Recreation</h2>
                <p>Get your kids active and engaged! From martial arts to gymnastics, multi-sport programs to fitness classes - find the perfect activity for your child.</p>
            </div>
            <div id="sports-recreation-resources" class="resources-grid"></div>
        </section>

        <!-- Arts & Self Expression Section -->
        <section id="arts-expression" class="section">
            <div class="section-header">
                <h2>🎨 Arts & Self Expression</h2>
                <p>Nurture creativity and confidence through drama, music, dance, and visual arts. Programs for all ages from toddlers to teens.</p>
            </div>
            <div id="arts-expression-resources" class="resources-grid"></div>
        </section>

        <!-- Rural & Remote Support Section -->
        <section id="rural-remote" class="section">
            <div class="section-header">
                <h2>🌾 Rural & Remote Support</h2>
                <p>Living outside the city? Access specialized support services, travel assistance, and resources designed for rural and remote families.</p>
            </div>
            <div id="rural-remote-resources" class="resources-grid"></div>
        </section>

'''

if ai_chat_idx != -1:
    html = html[:ai_chat_idx] + new_sections + '\n        ' + html[ai_chat_idx:]

# Write updated HTML
with open('index.html', 'w') as f:
    f.write(html)

print("✅ HTML updated successfully!")
print("Added new sections:")
print("  - Child Health")
print("  - Sports & Recreation")
print("  - Arts & Self Expression")
print("  - Rural & Remote Support")
print("Updated navigation with all sections")
print("Changed logo from 🤝 to 🏡")
print("Updated stylesheet to styles-new.css")