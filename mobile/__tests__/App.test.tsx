import React from 'react';
import {render, fireEvent, waitFor} from '@testing-library/react-native';
import App from '../App';

// Mock axios
jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({data: []})),
  post: jest.fn(() => Promise.resolve({data: {}})),
}));

describe('App', () => {
  it('renders correctly', () => {
    const {getByText} = render(<App />);
    expect(getByText('Feature Voting System')).toBeTruthy();
    expect(getByText('Add New Feature')).toBeTruthy();
  });

  it('shows form inputs', () => {
    const {getByPlaceholderText} = render(<App />);
    expect(getByPlaceholderText('Feature title')).toBeTruthy();
    expect(getByPlaceholderText('Feature description (optional)')).toBeTruthy();
  });

  it('shows create button', () => {
    const {getByText} = render(<App />);
    expect(getByText('Create Feature')).toBeTruthy();
  });

  it('shows features section', () => {
    const {getByText} = render(<App />);
    expect(getByText(/Features \(\d+\)/)).toBeTruthy();
  });
});