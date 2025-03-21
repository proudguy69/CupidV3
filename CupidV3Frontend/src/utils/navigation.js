import { inject } from "vue";
import router from '@/router';


export function toHome() {
    router.push('/')
}

export function toAuth(oauth_uri) {
    window.location.href = oauth_uri.value
}

export function toSignup() {
    router.push('/signup')
}

export function toSwipe() {
    router.push('/swipe')
}

export function removeAuth(userProfile, loggedIn) {
    fetch('/api/0auth/clear')
    userProfile.value = {}
    loggedIn.value = false
    router.replace('/')
}

export function toMatches() {
    router.push('/matches')
}