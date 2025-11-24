// Example JavaScript File
// This demonstrates common JavaScript patterns and features

// ES6+ Features
const greet = (name) => {
    return `Hello, ${name}! Welcome to JavaScript.`;
};

// Arrow functions and template literals
const calculateArea = (width, height) => width * height;

// Object destructuring
const user = {
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    age: 30
};

const { firstName, lastName, email } = user;
console.log(`User: ${firstName} ${lastName} (${email})`);

// Array methods
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
const sum = numbers.reduce((acc, n) => acc + n, 0);

// Async/await example
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching user data:', error);
        throw error;
    }
}

// Class definition
class Calculator {
    constructor() {
        this.history = [];
    }
    
    add(a, b) {
        const result = a + b;
        this.history.push({ operation: 'add', a, b, result });
        return result;
    }
    
    getHistory() {
        return this.history;
    }
}

// Export for module systems
export { greet, calculateArea, Calculator };

