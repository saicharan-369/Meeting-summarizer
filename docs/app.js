const BACKEND = (new URLSearchParams(window.location.search)).get('backend') || 'https://127.0.0.1:8000'

function $(id){return document.getElementById(id)}

// Navigation
const pages = ['home','login','upload','profile','assignment']
pages.forEach(p=>{
  $('nav-'+p).addEventListener('click', ()=>{
    pages.forEach(x=>$('nav-'+x).classList.remove('active'))
    $('nav-'+p).classList.add('active')
    pages.forEach(x=>$('page-'+x).classList.add('hidden'))
    $('page-'+p).classList.remove('hidden')
  })
})

// Login
$('btn-login').addEventListener('click', ()=>{
  const name = $('name').value.trim()
  const email = $('email').value.trim()
  if(!email){$('login-msg').innerText = 'Please enter email'; return}
  localStorage.setItem('user_name', name||email.split('@')[0])
  localStorage.setItem('user_email', email)
  $('login-msg').innerText = 'Signed in as '+localStorage.getItem('user_name')
})

// Upload
$('btn-upload').addEventListener('click', async ()=>{
  const f = $('file').files[0]
  if(!f){$('progress').innerText = 'Please choose a file.'; return}
  $('progress').innerText = 'Uploading...'
  const form = new FormData(); form.append('file', f)
  try{
    const resp = await fetch(BACKEND + '/upload-audio', {method:'POST', body: form})
    if(!resp.ok){const t=await resp.text(); throw new Error(t||resp.status)}
    const data = await resp.json()
    $('transcript').innerText = data.transcript || ''
    $('summary').innerText = data.summary || ''
    $('progress').innerText = 'Done'
  }catch(err){
    $('progress').innerText = 'Error: '+err.message
  }
})

// Assignment submit
$('btn-submit-assignment').addEventListener('click', ()=>{
  const link = $('assignment-link').value.trim()
  if(!link){$('assignment-msg').innerText='Please enter a link'; return}
  $('assignment-msg').innerText = 'Submitted (demo): '+link
})
