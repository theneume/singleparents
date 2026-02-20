// Load resources data
let resourcesData = {};
let knowledgeBase = {};
let conversationHistory = [];
let userName = null;

// Load JSON data
Promise.all([
    fetch('resources-data.json').then(response => response.json()),
    fetch('knowledge-base.json').then(response => response.json())
]).then(([resources, knowledge]) => {
    resourcesData = resources;
    knowledgeBase = knowledge;
    initializeApp();
}).catch(error => {
    console.error('Error loading data:', error);
});

// Initialize the application
function initializeApp() {
    setupNavigation();
    renderResources();
    setupChat();
}

// Navigation functionality
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = link.getAttribute('data-section');
            navigateToSection(sectionId);
        });
    });
}

function navigateToSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === sectionId) {
            link.classList.add('active');
        }
    });
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Render resource cards
function renderResources() {
    renderResourceSection('mental-health-resources', resourcesData.mentalHealth, '💙');
    renderResourceSection('legal-resources', resourcesData.legalServices, '⚖️');
    renderResourceSection('community-resources', resourcesData.communitySupport, '👥');
    renderResourceSection('child-development-resources', resourcesData.childDevelopment, '👶');
    renderResourceSection('mens-support-resources', resourcesData.mensSupport, '👨');
    renderResourceSection('family-events-resources', resourcesData.familyEvents, '🎉');
    renderResourceSection('child-health-resources', resourcesData.childHealth, '🏥');
    renderResourceSection('sports-recreation-resources', resourcesData.sportsRecreation, '⚽');
    renderResourceSection('arts-expression-resources', resourcesData.artsExpression, '🎨');
    renderResourceSection('alternative-education-resources', resourcesData.alternativeEducation, '🌱');
    renderResourceSection('alternative-health-resources', resourcesData.alternativeHealth, '🌿');
    renderResourceSection('alternative-childcare-resources', resourcesData.alternativeChildcare, '🏕️');
    renderResourceSection('rural-remote-resources', resourcesData.ruralRemote, '🌾');
    renderResourceSection('government-resources', resourcesData.governmentSupport, '🏛️');
    renderResourceSection('financial-resources', resourcesData.financialSupport, '💰');
    renderResourceSection('housing-resources', resourcesData.housingSupport, '🏠');
    renderResourceSection('mediation-resources', resourcesData.mediationServices, '🤝');
    renderResourceSection('emergency-resources', resourcesData.emergencySupport, '🚨');
}

function renderResourceSection(containerId, resources, icon) {
    const container = document.getElementById(containerId);
    if (!container || !resources) return;
    
    container.innerHTML = resources.map(resource => createResourceCard(resource, icon)).join('');
}

function createResourceCard(resource, icon) {
    const servicesHTML = resource.services 
        ? `<div class="resource-services">
               ${resource.services.map(service => `<span class="service-tag">${service}</span>`).join('')}
           </div>`
        : '';
    
    const phoneHTML = resource.phone 
        ? `<div class="contact-item">
               📞 <a href="tel:${resource.phone.replace(/\s/g, '')}">${resource.phone}</a>
           </div>`
        : '';
    
    const websiteHTML = resource.website 
        ? `<div class="contact-item">
               🌐 <a href="${resource.website}" target="_blank" rel="noopener noreferrer">Visit Website</a>
           </div>`
        : '';
    
    return `
        <div class="resource-card">
            <h3>${icon} ${resource.name}</h3>
            <span class="resource-type">${resource.type}</span>
            <p>${resource.description}</p>
            ${servicesHTML}
            <div class="contact-info">
                ${phoneHTML}
                ${websiteHTML}
            </div>
        </div>
    `;
}

// Chat functionality with Vertex AI and Real-Time Google Search
function setupChat() {
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send-btn');
    const chatMessages = document.getElementById('chat-messages');
    
    // Vertex AI Backend API endpoint
    const VERTEX_API_ENDPOINT = '/api/vertex-chat';
    
    // Send initial greeting
    setTimeout(() => {
        const greeting = `Hi! I'm here to support you through your journey as a single parent in Adelaide. 

I'd love to get to know you better - what's your name? And is there anything specific you'd like help with today? Whether it's finding support services, learning about events, or just having someone to talk to, I'm here for you. 😊`;
        addMessageToChat(greeting, 'assistant');
    }, 500);
    
    chatSendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Extract name from first message if not set
        if (!userName && conversationHistory.length === 0) {
            const nameMatch = message.match(/(?:my name is|i'm|i am|call me)\s+([a-zA-Z]+)/i);
            if (nameMatch) {
                userName = nameMatch[1];
            } else if (message.split(' ').length <= 3 && /^[a-zA-Z]+$/.test(message.trim())) {
                userName = message.trim();
            }
        }
        
        // Add to conversation history
        conversationHistory.push({
            role: 'user',
            content: message
        });
        
        addMessageToChat(message, 'user');
        chatInput.value = '';
        const loadingId = addLoadingMessage();
        
        try {
            const relevantKnowledge = extractRelevantKnowledge(message);
            
            // Call backend API with Vertex AI
            const response = await fetch(VERTEX_API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    userName: userName,
                    conversationHistory: conversationHistory.slice(-6),
                    relevantKnowledge: relevantKnowledge
                })
            });
            
            const data = await response.json();
            removeLoadingMessage(loadingId);
            
            if (data.response) {
                const aiResponse = data.response;
                
                // Add to conversation history
                conversationHistory.push({
                    role: 'assistant',
                    content: aiResponse
                });
                
                addMessageToChat(aiResponse, 'assistant');
            } else {
                addMessageToChat('I apologize, but I encountered an error. Please try again or contact one of the support services directly.', 'assistant');
            }
        } catch (error) {
            console.error('Chat error:', error);
            removeLoadingMessage(loadingId);
            addMessageToChat('I apologize, but I\'m having trouble connecting right now. Please try again later or contact one of the support services directly.', 'assistant');
        }
    }
    
    function extractRelevantKnowledge(message) {
        const messageLower = message.toLowerCase();
        let relevant = {};
        
        if (messageLower.includes('mental health') || messageLower.includes('counselling') || 
            messageLower.includes('depression') || messageLower.includes('anxiety') || 
            messageLower.includes('stress') || messageLower.includes('overwhelmed')) {
            relevant.mentalHealth = knowledgeBase.mentalHealthSupport;
        }
        
        if (messageLower.includes('legal') || messageLower.includes('lawyer') || 
            messageLower.includes('custody') || messageLower.includes('separation') || 
            messageLower.includes('divorce') || messageLower.includes('court')) {
            relevant.legal = knowledgeBase.legalSupport;
        }
        
        if (messageLower.includes('dad') || messageLower.includes('father') || 
            messageLower.includes('men') || messageLower.includes('single dad')) {
            relevant.mensSupport = knowledgeBase.mensSupport;
        }
        
        if (messageLower.includes('event') || messageLower.includes('activity') || 
            messageLower.includes('playgroup') || messageLower.includes('banana splitz') || 
            messageLower.includes('circle of security')) {
            relevant.familyEvents = knowledgeBase.familyEvents;
        }
        
        if (messageLower.includes('child') || messageLower.includes('parenting') || 
            messageLower.includes('development') || messageLower.includes('kids')) {
            relevant.childDevelopment = knowledgeBase.childDevelopment;
        }
        
        if (messageLower.includes('financial') || messageLower.includes('money') || 
            messageLower.includes('centrelink') || messageLower.includes('payment') || 
            messageLower.includes('support payment')) {
            relevant.financial = knowledgeBase.financialSupport;
        }
        
        if (messageLower.includes('housing') || messageLower.includes('accommodation') || 
            messageLower.includes('rent') || messageLower.includes('homeless')) {
            relevant.housing = knowledgeBase.housingSupport;
        }
        
        if (messageLower.includes('emergency') || messageLower.includes('crisis') || 
            messageLower.includes('urgent') || messageLower.includes('help now')) {
            relevant.emergency = knowledgeBase.emergencyServices;
        }
        
        if (messageLower.includes('health') || messageLower.includes('doctor') || 
            messageLower.includes('medical') || messageLower.includes('immunisation') || 
            messageLower.includes('sick') || messageLower.includes('cafhs')) {
            relevant.childHealth = knowledgeBase.child_health;
        }
        
        if (messageLower.includes('sport') || messageLower.includes('recreation') || 
            messageLower.includes('martial arts') || messageLower.includes('gymnastics') || 
            messageLower.includes('fitness') || messageLower.includes('active') || 
            messageLower.includes('exercise')) {
            relevant.sportsRecreation = knowledgeBase.sports_recreation;
        }
        
        if (messageLower.includes('art') || messageLower.includes('music') || 
            messageLower.includes('dance') || messageLower.includes('drama') || 
            messageLower.includes('creative') || messageLower.includes('theatre') || 
            messageLower.includes('pottery') || messageLower.includes('expression')) {
            relevant.artsExpression = knowledgeBase.arts_expression;
        }
        
        if (messageLower.includes('rural') || messageLower.includes('remote') || 
            messageLower.includes('regional') || messageLower.includes('country')) {
            relevant.ruralRemote = knowledgeBase.rural_remote;
        }
        
        if (messageLower.includes('montessori') || messageLower.includes('steiner') || 
            messageLower.includes('waldorf') || messageLower.includes('alternative school') ||
            messageLower.includes('alternative education') || messageLower.includes('forest school') ||
            messageLower.includes('nature school') || messageLower.includes('homeschool')) {
            relevant.alternativeEducation = knowledgeBase.alternative_education;
        }
        
        if (messageLower.includes('naturopath') || messageLower.includes('homeopath') || 
            messageLower.includes('chiropract') || messageLower.includes('osteopath') ||
            messageLower.includes('alternative health') || messageLower.includes('natural health') ||
            messageLower.includes('herbal') || messageLower.includes('holistic health') ||
            messageLower.includes('tcm') || messageLower.includes('chinese medicine')) {
            relevant.alternativeHealth = knowledgeBase.alternative_health;
        }
        
        if (messageLower.includes('nature play') || messageLower.includes('forest school') ||
            messageLower.includes('alternative childcare') || messageLower.includes('outdoor care') ||
            messageLower.includes('nature-based care') || messageLower.includes('waldorf playgroup') ||
            messageLower.includes('montessori childcare')) {
            relevant.alternativeChildcare = knowledgeBase.alternative_childcare;
        }
        
        return relevant;
    }
    
    function addMessageToChat(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatar = sender === 'user' ? '👤' : '🤖';
        
        // Convert markdown-style links to HTML
        let formattedText = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
        
        // Convert **bold** to HTML
        formattedText = formattedText.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        // Convert URLs to clickable links
        formattedText = formattedText.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
        
        // Format text for better readability:
        // 1. Split into paragraphs by double newlines
        // 2. Wrap each paragraph in <p> tags
        // 3. Handle single line breaks within paragraphs
        const paragraphs = formattedText.split(/\n\s*\n/);
        const formattedParagraphs = paragraphs.map(para => {
            // Replace single newlines with spaces within paragraphs
            let cleanPara = para.replace(/\n/g, ' ');
            // Remove extra spaces
            cleanPara = cleanPara.replace(/\s+/g, ' ').trim();
            return cleanPara ? `<p style="margin-bottom: 1em; line-height: 1.6;">${cleanPara}</p>` : '';
        }).join('');
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                ${formattedParagraphs}
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function addLoadingMessage() {
        const loadingId = 'loading-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        messageDiv.id = loadingId;
        
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="loading"></div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return loadingId;
    }
    
    function removeLoadingMessage(loadingId) {
        const loadingMsg = document.getElementById(loadingId);
        if (loadingMsg) loadingMsg.remove();
    }
}

function formatPhoneNumber(phone) {
    return phone.replace(/\s/g, '');
}

function searchResources(query) {
    const lowerQuery = query.toLowerCase();
    const results = [];
    
    Object.keys(resourcesData).forEach(category => {
        resourcesData[category].forEach(resource => {
            if (resource.name.toLowerCase().includes(lowerQuery) ||
                resource.description.toLowerCase().includes(lowerQuery) ||
                (resource.services && resource.services.some(s => s.toLowerCase().includes(lowerQuery)))) {
                results.push({ ...resource, category });
            }
        });
    });
    
    return results;
}

window.navigateToSection = navigateToSection;
window.searchResources = searchResources;

console.log('%c✨ Adelaide Single Parents Connect - Vertex AI with Real-Time Search', 'color: #e8927c; font-size: 20px; font-weight: bold;');
console.log('%cApp initialized with Vertex AI and Google Search grounding!', 'color: #a8d5ba; font-size: 14px;');