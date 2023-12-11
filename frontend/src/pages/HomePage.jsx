import React from 'react';
import NavBar from './components/NavBar';
import ImageSection from './components/ImageSection'; // Adicione esta linha
import MainSection from './components/MainSection';

const HomePage = () => {
    return (
        <>
            <NavBar />
            <div style={{ backgroundColor: 'white' }}>
                <div style={{ display: 'flex' }}>
                    <ImageSection />
                    <MainSection />
                </div>
            </div>
        </>
    );
};

export default HomePage;

