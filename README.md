# Adelaide Single Parents Connect

A comprehensive web platform supporting single parents in Adelaide, South Australia with resources, AI chat, and community services.

## Features

- 📚 **88+ Resources** across 18 categories including alternative education, health, and childcare
- 🤖 **AI-Powered Chat** with Vertex AI and Google Search integration
- 🌱 **Alternative Approaches**: Montessori, Steiner, nature-based education, holistic health
- 💬 **Real-time Support** with knowledge base and web search
- 🎨 **Modern Design** with orange color scheme and responsive layout

## Deployment

### Quick Deploy to Render

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Set your environment variables:
     - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID
     - `GOOGLE_CLOUD_LOCATION`: `us-central1` (or your preferred region)

3. **Add Google Cloud Credentials**
   - In Google Cloud Console, create a service account key
   - Download the JSON file
   - In Render dashboard, add environment variable:
     - `GOOGLE_APPLICATION_CREDENTIALS`: Paste the entire JSON content

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_CLOUD_PROJECT` | Google Cloud Project ID | Yes | - |
| `GOOGLE_CLOUD_LOCATION` | Google Cloud region | No | `us-central1` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account credentials JSON | Yes | - |
| `PORT` | Port number | No | `10000` |

## Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   Create a `.env` file:
   ```bash
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_APPLICATION_CREDENTIALS='{"type": "service_account", ...}'
   ```

3. **Run the server**
   ```bash
   python vertex_api_server.py
   ```

4. **Access the application**
   - Open http://localhost:8052 in your browser

## Project Structure

```
.
├── index.html              # Main application HTML
├── styles.css              # Styling (orange theme)
├── app-vertex-ai.js        # Frontend JavaScript with AI chat
├── vertex_api_server.py    # Flask backend with Vertex AI
├── resources-data.json     # 88+ resources database
├── knowledge-base.json     # Comprehensive knowledge base
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
├── .gitignore              # Git ignore rules
└── README.md              # This file
```

## Resource Categories

1. 🏠 Home
2. 💙 Mental Health
3. ⚖️ Legal Support
4. 👥 Community
5. 🏥 Child Health
6. 👶 Child Development
7. ⚽ Sports & Recreation
8. 🎨 Arts & Expression
9. 👨 Men's Support
10. 🎉 Family Events
11. 🌱 Alternative Education
12. 🌿 Alternative Health
13. 🏕️ Alternative Childcare
14. 🌾 Rural & Remote
15. 💰 Financial Help
16. 🚨 Emergency
17. 💬 AI Support Chat

## Features

### AI Chat
- Vertex AI integration with Google Search grounding
- Conversation memory and context
- Real-time web search for events and current information
- Detailed knowledge base for accurate responses
- Clean, formatted responses with proper spacing

### Design
- Modern, responsive layout
- Orange color scheme (#ff8c42)
- House icon (🏡)
- Donate and contact buttons in header
- Mobile-friendly navigation

### Alternative Approaches
- Montessori education options
- Steiner/Waldorf schools
- Forest schools and nature-based learning
- Naturopathy and homeopathy
- Chiropractic and osteopathy
- Holistic childcare options

## Support

- **Donate**: https://donate.stripe.com/6oU3cv2aK1lkcjK1DH43S00
- **Contact**: deepsyketech@proton.me

## License

This project is provided as-is for the benefit of single parents in Adelaide.