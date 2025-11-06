import { v4 as uuidv4 } from 'uuid';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = "http://localhost:8000" //"http://<your-local-ip>:8000";

export const getUserId = async (): Promise<string> => {
  let userId = await AsyncStorage.getItem('userId');
  if (!userId) {
    userId = uuidv4();
    await AsyncStorage.setItem('userId', userId);
  }
  return userId;
};

export const fetchChatHistory = async (userId: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/history/${userId}`);
    if (!response.ok) throw new Error('Failed to load history');
    return await response.json();
  } catch (error) {
    console.error('fetchChatHistory error:', error);
    return [];
  }
};

export const sendChatMessage = async (userId: string, message: string) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, message }),
    });
    if (!response.ok) throw new Error('Failed to send message');
    return await response.json();
  } catch (error) {
    console.error('sendChatMessage error:', error);
    return { response: 'Something went wrong. Please try again.' };
  }
};
