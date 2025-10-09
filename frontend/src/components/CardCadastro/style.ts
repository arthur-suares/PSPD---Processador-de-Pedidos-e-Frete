import styled from "styled-components";

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 1200px;
  margin: 5vh;
  gap: 1rem;
  background-color: white;
  padding: 2rem;
  border-radius: 28px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

  h5 {
    font-weight: 300;
    font-size: 1rem;
  }
`;

export const Title = styled.h1`
  font-size: 2.5rem;
  margin: 0;
  font-weight: normal;
  font-family: 'Impact', sans-serif;  
  color: #BE6E46;
`;

export const Label = styled.label`
  font-size: 1rem;
  font-weight: bold;
  color: #333;
`;

export const Input = styled.input`
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;

  &:focus {
    border-color: #BE6E46;
  }
`;

export const TextArea = styled.textarea`
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
  outline: none;

  &:focus {
    border-color: #BE6E46;
  }
`;

export const Button = styled.button`
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  color: white;
  background-color: #BE6E46;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #004c2e;
  }
`;

export const Select = styled.select`
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
`;
