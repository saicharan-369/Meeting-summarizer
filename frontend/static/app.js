const BACKEND = (new URLSearchParams(window.location.search)).get('backend') || 'http://127.0.0.1:8000'

function $(id) { return document.getElementById(id) }

// Navigation - All pages
const pages = ['home', 'login', 'upload', 'history', 'profile']
pages.forEach(p => {
  const navBtn = $('nav-' + p)
  if (navBtn) {
    navBtn.addEventListener('click', () => {
      // Hide all pages
      pages.forEach(x => {
        const nav = $('nav-' + x)
        const page = $('page-' + x)
        if (nav) nav.classList.remove('active')
        if (page) page.classList.add('hidden')
      })
      // Show selected page
      navBtn.classList.add('active')
      const page = $('page-' + p)
      if (page) page.classList.remove('hidden')
      
      // Scroll to top smoothly
      window.scrollTo({ top: 0, behavior: 'smooth' })
    })
  }
})

// Hero upload button
const heroUploadBtn = $('hero-upload-btn')
if (heroUploadBtn) {
  heroUploadBtn.addEventListener('click', () => {
    $('nav-upload').click()
  })
}

// Drag & Drop functionality
const dropzone = $('dropzone')
const fileInput = $('file')
const browseBtn = $('browse-btn')
const fileSelected = $('file-selected')
const uploadBtn = $('btn-upload')
const progressContainer = $('progress')
const resultsContainer = $('results')

let selectedFile = null

// Browse button
if (browseBtn) {
  browseBtn.addEventListener('click', (e) => {
    e.stopPropagation()
    fileInput.click()
  })
}

// Dropzone click
if (dropzone) {
  dropzone.addEventListener('click', () => {
    fileInput.click()
  })
}

// Drag over
if (dropzone) {
  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault()
    dropzone.classList.add('drag-over')
  })

  dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('drag-over')
  })

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault()
    dropzone.classList.remove('drag-over')
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileSelect(files[0])
    }
  })
}

// File input change
if (fileInput) {
  fileInput.addEventListener('change', (e) => {
    const files = e.target.files
    if (files.length > 0) {
      handleFileSelect(files[0])
    }
  })
}

// Handle file selection
function handleFileSelect(file) {
  // Check if WAV file
  if (!file.name.toLowerCase().endsWith('.wav')) {
    alert('⚠️ Please upload WAV files only!\n\nConvert MP3 to WAV at:\nhttps://online-audio-converter.com/')
    return
  }

  selectedFile = file
  
  // Show file info
  dropzone.style.display = 'none'
  fileSelected.classList.remove('hidden')
  $('file-name').textContent = file.name
  $('file-size').textContent = formatFileSize(file.size)
  
  // Enable upload button
  uploadBtn.disabled = false
}

// Remove file
const removeFileBtn = $('remove-file')
if (removeFileBtn) {
  removeFileBtn.addEventListener('click', () => {
    selectedFile = null
    fileInput.value = ''
    dropzone.style.display = 'block'
    fileSelected.classList.add('hidden')
    uploadBtn.disabled = true
    resultsContainer.classList.add('hidden')
  })
}

// Format file size
function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// Upload & Process
if (uploadBtn) {
  uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) {
      alert('Please select a file first')
      return
    }

    // Hide results
    resultsContainer.classList.add('hidden')

    // Show progress
    progressContainer.classList.remove('hidden')
    const progressFill = $('progress-fill')
    const progressText = $('progress-text')
    
    progressFill.style.width = '0%'
    progressText.textContent = 'Uploading...'

    // Simulate upload progress
    let progress = 0
    const progressInterval = setInterval(() => {
      progress += 10
      if (progress <= 90) {
        progressFill.style.width = progress + '%'
      }
    }, 200)

    // Upload file
    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch(BACKEND + '/upload-audio', {
        method: 'POST',
        body: formData
      })

      clearInterval(progressInterval)
      progressFill.style.width = '100%'

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(errorText || `HTTP ${response.status}`)
      }

      const data = await response.json()

      // Show success
      progressText.textContent = '✅ Transcription complete!'
      
      // Wait a moment then hide progress and show results
      setTimeout(() => {
        progressContainer.classList.add('hidden')
        
        // Display results
        $('transcript').textContent = data.transcript || 'No transcript available'
        $('summary').textContent = data.summary || 'No summary available'
        resultsContainer.classList.remove('hidden')
        
        // Save to history
        const filename = selectedFile ? selectedFile.name : 'Unknown'
        saveToHistory(filename, data.transcript, data.summary)
        loadHistory()
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 1000)

    } catch (error) {
      clearInterval(progressInterval)
      progressText.textContent = '❌ Error: ' + error.message
      progressFill.style.width = '100%'
      progressFill.style.background = 'var(--error)'
      
      console.error('Upload error:', error)
    }
  })
}

// Copy buttons
const copyTranscriptBtn = $('copy-transcript')
const copySummaryBtn = $('copy-summary')

if (copyTranscriptBtn) {
  copyTranscriptBtn.addEventListener('click', () => {
    const text = $('transcript').textContent
    navigator.clipboard.writeText(text).then(() => {
      copyTranscriptBtn.innerHTML = `
        <svg class="btn-icon-sm" viewBox="0 0 24 24" fill="none">
          <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Copied!
      `
      setTimeout(() => {
        copyTranscriptBtn.innerHTML = `
          <svg class="btn-icon-sm" viewBox="0 0 24 24" fill="none">
            <rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/>
            <path d="M5 15H4C3.46957 15 3 14.5304 3 14V4C3 3.46957 3.46957 3 4 3H14C14.5304 3 15 3.46957 15 4V5" stroke="currentColor" stroke-width="2"/>
          </svg>
          Copy
        `
      }, 2000)
    })
  })
}

if (copySummaryBtn) {
  copySummaryBtn.addEventListener('click', () => {
    const text = $('summary').textContent
    navigator.clipboard.writeText(text).then(() => {
      copySummaryBtn.innerHTML = `
        <svg class="btn-icon-sm" viewBox="0 0 24 24" fill="none">
          <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Copied!
      `
      setTimeout(() => {
        copySummaryBtn.innerHTML = `
          <svg class="btn-icon-sm" viewBox="0 0 24 24" fill="none">
            <rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/>
            <path d="M5 15H4C3.46957 15 3 14.5304 3 14V4C3 3.46957 3.46957 3 4 3H14C14.5304 3 15 3.46957 15 4V5" stroke="currentColor" stroke-width="2"/>
          </svg>
          Copy
        `
      }, 2000)
    })
  })
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault()
    const target = document.querySelector(this.getAttribute('href'))
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' })
    }
  })
})

console.log('🎉 Meeting Summarizer loaded!')
console.log('Backend:', BACKEND)

// ============================================
// LOGIN & AUTHENTICATION
// ============================================

// Check login status on page load
function checkLoginStatus() {
  // Skip login - set default user for everyone
  const userName = localStorage.getItem('user_name') || 'Guest User'
  const userEmail = localStorage.getItem('user_email') || 'guest@example.com'
  
  // Auto-login everyone
  localStorage.setItem('user_name', userName)
  localStorage.setItem('user_email', userEmail)
  
  // Always show logged in nav
  showLoggedInNav()
  updateProfileInfo(userName, userEmail)
  loadHistory()
}

// Show login page for non-authenticated users (DISABLED)
function showLoginPage() {
  // Login disabled - redirect to home
  const navHome = $('nav-home')
  if (navHome) navHome.click()
}

function showLoggedInNav() {
  const navLogin = $('nav-login')
  const navUpload = $('nav-upload')
  const navHistory = $('nav-history')
  const navProfile = $('nav-profile')
  const btnLogout = $('btn-logout')
  
  // Hide login permanently
  if (navLogin) navLogin.style.display = 'none'
  // Show all other navigation
  if (navUpload) navUpload.style.display = 'inline-block'
  if (navHistory) navHistory.style.display = 'inline-block'
  if (navProfile) navProfile.style.display = 'inline-block'
  // Hide logout button (no login needed)
  if (btnLogout) btnLogout.style.display = 'none'
}

function showLoggedOutNav() {
  const navLogin = $('nav-login')
  const navUpload = $('nav-upload')
  const navHistory = $('nav-history')
  const navProfile = $('nav-profile')
  const btnLogout = $('btn-logout')
  
  if (navLogin) navLogin.style.display = 'inline-block'
  if (navUpload) navUpload.style.display = 'none'
  if (navHistory) navHistory.style.display = 'none'
  if (navProfile) navProfile.style.display = 'none'
  if (btnLogout) btnLogout.style.display = 'none'
}

// Hero login button - redirect to upload
const heroLoginBtn = $('hero-login-btn')
if (heroLoginBtn) {
  heroLoginBtn.addEventListener('click', () => {
    const navUpload = $('nav-upload')
    if (navUpload) navUpload.click()
  })
}

// Login form handler
const btnLogin = $('btn-login')
if (btnLogin) {
  btnLogin.addEventListener('click', () => {
    const loginName = $('login-name')
    const loginEmail = $('login-email')
    const loginMsg = $('login-msg')
    
    if (!loginName || !loginEmail || !loginMsg) return
    
    const name = loginName.value.trim()
    const email = loginEmail.value.trim()
    
    if (!name) {
      loginMsg.textContent = '⚠️ Please enter your name'
      loginMsg.style.background = 'rgba(239, 68, 68, 0.2)'
      return
    }
    
    if (!email || !email.includes('@')) {
      loginMsg.textContent = '⚠️ Please enter a valid email'
      loginMsg.style.background = 'rgba(239, 68, 68, 0.2)'
      return
    }
    
    // Save to localStorage
    localStorage.setItem('user_name', name)
    localStorage.setItem('user_email', email)
    
    // Show success message
    loginMsg.textContent = `✅ Welcome, ${name}!`
    loginMsg.style.background = 'rgba(34, 197, 94, 0.2)'
    
    // Update UI after a moment
    setTimeout(() => {
      showLoggedInNav()
      updateProfileInfo(name, email)
      const navUpload = $('nav-upload')
      if (navUpload) navUpload.click()
    }, 1000)
  })
}

// Logout handler
const btnLogout = $('btn-logout')
if (btnLogout) {
  btnLogout.addEventListener('click', () => {
    if (confirm('Are you sure you want to logout?')) {
      localStorage.removeItem('user_name')
      localStorage.removeItem('user_email')
      showLoggedOutNav()
      showLoginPage()
      
      // Clear form
      const loginName = $('login-name')
      const loginEmail = $('login-email')
      const loginMsg = $('login-msg')
      if (loginName) loginName.value = ''
      if (loginEmail) loginEmail.value = ''
      if (loginMsg) loginMsg.textContent = ''
    }
  })
}

// ============================================
// HISTORY TRACKING (USER-SPECIFIC)
// ============================================

// Get user-specific history key
function getUserHistoryKey() {
  const userEmail = localStorage.getItem('user_email')
  if (!userEmail) return null
  // Use email as unique identifier for history
  return 'transcription_history_' + userEmail.replace(/[^a-zA-Z0-9]/g, '_')
}

function saveToHistory(filename, transcript, summary) {
  const historyKey = getUserHistoryKey()
  if (!historyKey) {
    console.warn('Cannot save history: User not logged in')
    return
  }
  
  const history = JSON.parse(localStorage.getItem(historyKey) || '[]')
  
  const item = {
    id: Date.now(),
    filename: filename,
    transcript: transcript,
    summary: summary,
    date: new Date().toISOString(),
    dateFormatted: new Date().toLocaleString(),
    userEmail: localStorage.getItem('user_email') // Store which user created this
  }
  
  history.unshift(item) // Add to beginning
  
  // Keep only last 50 items per user
  if (history.length > 50) {
    history.pop()
  }
  
  localStorage.setItem(historyKey, JSON.stringify(history))
  updateTranscriptionCount()
}

function loadHistory() {
  const historyKey = getUserHistoryKey()
  if (!historyKey) {
    console.warn('Cannot load history: User not logged in')
    return
  }
  
  const history = JSON.parse(localStorage.getItem(historyKey) || '[]')
  const historyList = $('history-list')
  const historyEmpty = $('history-empty')
  
  if (!historyList || !historyEmpty) return
  
  if (history.length === 0) {
    historyList.style.display = 'none'
    historyEmpty.style.display = 'block'
    return
  }
  
  historyList.style.display = 'flex'
  historyEmpty.style.display = 'none'
  historyList.innerHTML = ''
  
  history.forEach(item => {
    const itemEl = document.createElement('div')
    itemEl.className = 'history-item glass-effect'
    itemEl.innerHTML = `
      <div class="history-item-header">
        <span class="history-item-title">🎙️ ${item.filename}</span>
        <span class="history-item-date">${item.dateFormatted}</span>
      </div>
      <div class="history-item-preview">${item.transcript.substring(0, 150)}...</div>
      <div class="history-item-actions">
        <button class="btn btn-sm btn-outline" onclick="viewHistoryItem(${item.id})">
          View Full
        </button>
        <button class="btn btn-sm btn-outline" onclick="deleteHistoryItem(${item.id})">
          Delete
        </button>
      </div>
    `
    historyList.appendChild(itemEl)
  })
}

window.viewHistoryItem = function(id) {
  const historyKey = getUserHistoryKey()
  if (!historyKey) return
  
  const history = JSON.parse(localStorage.getItem(historyKey) || '[]')
  const item = history.find(h => h.id === id)
  
  if (item) {
    $('transcript').textContent = item.transcript
    $('summary').textContent = item.summary
    resultsContainer.classList.remove('hidden')
    const navUpload = $('nav-upload')
    if (navUpload) navUpload.click()
    resultsContainer.scrollIntoView({ behavior: 'smooth' })
  }
}

window.deleteHistoryItem = function(id) {
  if (confirm('Delete this transcription?')) {
    const historyKey = getUserHistoryKey()
    if (!historyKey) return
    
    let history = JSON.parse(localStorage.getItem(historyKey) || '[]')
    history = history.filter(h => h.id !== id)
    localStorage.setItem(historyKey, JSON.stringify(history))
    loadHistory()
    updateTranscriptionCount()
  }
}

// Clear all history
const btnClearHistory = $('btn-clear-history')
if (btnClearHistory) {
  btnClearHistory.addEventListener('click', () => {
    if (confirm('Clear all transcription history? This cannot be undone.')) {
      const historyKey = getUserHistoryKey()
      if (historyKey) {
        localStorage.setItem(historyKey, '[]')
        loadHistory()
        updateTranscriptionCount()
      }
    }
  })
}

// History upload button
const historyUploadBtn = $('history-upload-btn')
if (historyUploadBtn) {
  historyUploadBtn.addEventListener('click', () => {
    const navUpload = $('nav-upload')
    if (navUpload) navUpload.click()
  })
}

// ============================================
// PROFILE UPDATES
// ============================================

function updateProfileInfo(name, email) {
  const profileName = $('profile-name')
  const profileEmail = $('profile-email')
  
  if (profileName) profileName.textContent = name
  if (profileEmail) profileEmail.textContent = email
  
  updateTranscriptionCount()
}

function updateTranscriptionCount() {
  const historyKey = getUserHistoryKey()
  if (!historyKey) {
    const statElement = $('stat-transcriptions')
    if (statElement) statElement.textContent = '0'
    return
  }
  
  const history = JSON.parse(localStorage.getItem(historyKey) || '[]')
  const statElement = $('stat-transcriptions')
  if (statElement) {
    statElement.textContent = history.length
  }
}

// ============================================
// NAVIGATION FOR NEW PAGES
// ============================================

// Add login and history to pages array
const additionalPages = ['login', 'history']
additionalPages.forEach(p => {
  const navBtn = $('nav-' + p)
  if (navBtn) {
    navBtn.addEventListener('click', () => {
      // Hide all pages
      ;['home', 'upload', 'profile', 'login', 'history'].forEach(x => {
        const nav = $('nav-' + x)
        const page = $('page-' + x)
        if (nav) nav.classList.remove('active')
        if (page) page.classList.add('hidden')
      })
      // Show selected page
      navBtn.classList.add('active')
      const page = $('page-' + p)
      if (page) page.classList.remove('hidden')
      
      // Load history if on history page
      if (p === 'history') {
        loadHistory()
      }
      
      // Scroll to top smoothly
      window.scrollTo({ top: 0, behavior: 'smooth' })
    })
  }
})

// ============================================
// INITIALIZE ON PAGE LOAD
// ============================================

checkLoginStatus()
