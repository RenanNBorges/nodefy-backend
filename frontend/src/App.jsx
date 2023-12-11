import React from 'react';
import { createRoot } from 'react-dom/client';
import HomePage from './pages/HomePage';

const App = () => {
    return (
        <div>
            <HomePage />
        </div>
    );
};

const container = document.getElementById('app');
const root = createRoot(container);
root.render(<App />); // Remova a propriedade 'tab'

export default App;
