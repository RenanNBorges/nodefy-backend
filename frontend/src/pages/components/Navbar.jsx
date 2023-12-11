import React from 'react';
import styled from 'styled-components';

const NavBar = () => {
  return (
    <NavbarContainer>
      <NavbarText>Nodefy+ Social Media</NavbarText>
      <LoginContainer>
        <Input placeholder="Usuário" />
        <Input placeholder="Senha" type="password" />
        <LoginButton>Login</LoginButton>
      </LoginContainer>
    </NavbarContainer>
  );
};

const NavbarContainer = styled.div`
  background-color: #c3e6cb; /* Tom de verde pastel */
  display: flex;
  justify-content: space-between;
  padding: 10px;
`;

const NavbarText = styled.div`
  font-size: 20px;
`;

const LoginContainer = styled.div`
  display: flex;
  align-items: center;
`;

const Input = styled.input`
  margin-right: 10px;
  padding: 5px;
`;

const LoginButton = styled.button`
  background-color: #007bff; /* Cor do botão (azul) */
  color: white;
  padding: 5px 10px;
  cursor: pointer;
`;

export default NavBar;
