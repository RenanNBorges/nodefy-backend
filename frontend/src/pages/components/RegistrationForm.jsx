import React from 'react';
import styled from 'styled-components';

const RegistrationForm = ({ isOrganization }) => {
    return (
        <FormContainer>
            <InputLabel>Nome:</InputLabel>
            <Input type="text" placeholder="Digite seu nome" />

            <InputLabel>Sobrenome:</InputLabel>
            <Input type="text" placeholder="Digite seu sobrenome" />

            <InputLabel>Data de Nascimento:</InputLabel>
            <Input type="date" />

            {/* Outros campos específicos para Pessoa */}
            {!isOrganization && (
                <>
                    <InputLabel>Número de Telefone:</InputLabel>
                    <Input type="tel" placeholder="Digite seu número de telefone" />
                </>
            )}

            {/* Campos específicos para Organização */}
            {isOrganization && (
                <>
                    <InputLabel>Tipo de Organização:</InputLabel>
                    <Input type="text" placeholder="Digite o tipo de organização" />

                    <InputLabel>Área de Atuação:</InputLabel>
                    <Input type="text" placeholder="Digite a área de atuação" />

                    <InputLabel>Site da Organização:</InputLabel>
                    <Input type="text" placeholder="Digite o site da organização" />
                </>
            )}
        </FormContainer>
    );
};

const FormContainer = styled.div`
    margin-bottom: 20px;
`;

const InputLabel = styled.div`
  margin-top: 10px;
`;

const Input = styled.input`
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
`;

export default RegistrationForm;
