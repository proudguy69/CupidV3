import { inject } from "vue";
import router from '@/router';


export function toHome() {
    router.push('/')
}

export function toAuth() {
    const oauth_uri = inject('oauth_uri')
    window.location.href = oauth_uri.value
}

export function toSignup() {
    router.push('/signup')
}

export function toSwipe() {
    router.push('/swipe')
}

export function removeAuth() {
    const userProfile = inject('userProfile')
    fetch('/api/0auth/clear')
    userProfile.value = {}
    loggedIn.value = false
    router.replace('/')
}

export function toMatches() {
    router.push('/matches')
}