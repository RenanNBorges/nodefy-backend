import React, { useState } from 'react';
import styled from 'styled-components';
import RegistrationForm from './RegistrationForm';

const MainSection = () => {
    const [isOrganization, setIsOrganization] = useState(false);

    return (
        <MainContainer>
            <Title>Ainda não tem cadastro?</Title>
            <RegistrationForm isOrganization={isOrganization} />
            <CheckboxContainer>
                <Checkbox
                    type="checkbox"
                    checked={isOrganization}
                    onChange={() => setIsOrganization(!isOrganization)}
                />
                <CheckboxLabel>É uma Organização?</CheckboxLabel>
            </CheckboxContainer>
            <SubmitButton>Submeter</SubmitButton>
        </MainContainer>
    );
};

const MainContainer = styled.div`
  flex: 1;
  padding: 20px;
`;

const Title = styled.div`
  font-size: 18px;
  margin-bottom: 10px;
`;

const CheckboxContainer = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 10px;
`;

const Checkbox = styled.input``;

const CheckboxLabel = styled.label`
  margin-left: 5px;
`;

const SubmitButton = styled.button`
  background-color: #007bff; /* Cor do botão (azul) */
  color: white;
  padding: 10px 20px;
  cursor: pointer;
`;

export default MainSection;
