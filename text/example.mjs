// ES Module JavaScript File (.mjs)
// This file uses ES6 module syntax

// Named exports
export function createUser(name, email) {
    return {
        id: Date.now(),
        name,
        email,
        createdAt: new Date().toISOString()
    };
}

export const API_BASE_URL = 'https://api.example.com/v1';

// Default export
export default class UserService {
    constructor(apiUrl = API_BASE_URL) {
        this.apiUrl = apiUrl;
        this.users = [];
    }
    
    async fetchUsers() {
        try {
            const response = await fetch(`${this.apiUrl}/users`);
            const data = await response.json();
            this.users = data;
            return data;
        } catch (error) {
            console.error('Failed to fetch users:', error);
            throw error;
        }
    }
    
    addUser(user) {
        this.users.push(user);
        return user;
    }
    
    findUserById(id) {
        return this.users.find(user => user.id === id);
    }
}

// Utility functions
export const formatDate = (date) => {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
};

export const validateEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
};

