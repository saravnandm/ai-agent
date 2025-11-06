import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  TextInput,
  Button,
  FlatList,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Image,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import {sendChatMessage, fetchChatHistory, getUserId} from './agentApi';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  time: Date;
}

export default function ChatScreen() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [userId, setUserId] = useState('');

  useEffect(() => {
    (async () => {
      const id = await getUserId();
      setUserId(id);
      const history = await fetchChatHistory(id);
      setChatHistory(history);
    })();
  }, []);

  const handleSend = async () => {
    if (!message.trim()) return;
    const userMsg: ChatMessage = {
      role: 'user',
      content: message,
      time: new Date(),
    };
    setChatHistory(prev => [...prev, userMsg]);
    setMessage('');

    const reply = await sendChatMessage(userId, message);

    const botMsg: ChatMessage = {
      role: 'assistant',
      content: reply?.reply || reply || '...',
      time: new Date(),
    };
    setChatHistory(prev => [...prev, botMsg]);
  };

  const renderItem = ({item}: any) => {
    const isUser = item.role === 'user';
    const time = new Date(item.time).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });

    return (
      <View
        style={[
          styles.messageWrapper,
          isUser ? styles.userWrapper : styles.assistantWrapper,
        ]}>
        {!isUser && (
          <Image
            source={{
              uri: 'https://cdn-icons-png.flaticon.com/512/4712/4712109.png',
            }}
            style={styles.avatar}
          />
        )}
        <View
          style={[
            styles.messageBubble,
            isUser ? styles.userBubble : styles.assistantBubble,
          ]}>
          <Text style={styles.messageText}>{item.content}</Text>
          <Text style={styles.timestamp}>{time}</Text>
        </View>
        {isUser && (
          <Image
            source={{
              uri: 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
            }}
            style={styles.avatar}
          />
        )}
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.safeArea} edges={['bottom']}>
      <KeyboardAvoidingView
        style={styles.container}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={90}>
        <FlatList
          data={chatHistory}
          keyExtractor={(_, i) => i.toString()}
          renderItem={renderItem}
          contentContainerStyle={styles.chatContent}
        />
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            value={message}
            placeholder="Type your message..."
            onChangeText={setMessage}
          />
          <Button title="Send" onPress={handleSend} />
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {flex: 1, backgroundColor: '#fff'},
  container: {flex: 1},
  chatContent: {padding: 10, flexGrow: 1},
  messageWrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    marginVertical: 4,
  },
  userWrapper: {alignSelf: 'flex-end', flexDirection: 'row-reverse'},
  assistantWrapper: {alignSelf: 'flex-start'},
  avatar: {width: 30, height: 30, borderRadius: 15, marginHorizontal: 6},
  messageBubble: {
    padding: 10,
    borderRadius: 12,
    maxWidth: '75%',
  },
  userBubble: {
    backgroundColor: '#DCF8C6',
    borderBottomRightRadius: 0,
  },
  assistantBubble: {
    backgroundColor: '#F1F0F0',
    borderBottomLeftRadius: 0,
  },
  messageText: {fontSize: 14, color: '#000'},
  timestamp: {
    fontSize: 11,
    color: '#555',
    alignSelf: 'flex-end',
    marginTop: 4,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderTopWidth: 1,
    borderColor: '#ddd',
    padding: 8,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 25,
    paddingHorizontal: 15,
    paddingVertical: 8,
    marginRight: 8,
  },
});
