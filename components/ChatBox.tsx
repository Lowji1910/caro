import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { ChatMessage } from '../types';

interface ChatBoxProps {
    messages: ChatMessage[];
    currentUserId: number;
    onSendMessage: (message: string) => void;
    disabled?: boolean;
}

const ChatBox: React.FC<ChatBoxProps> = ({ messages, currentUserId, onSendMessage, disabled }) => {
    const [newMessage, setNewMessage] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = () => {
        if (newMessage.trim() && !disabled) {
            onSendMessage(newMessage);
            setNewMessage('');
            // Reset height
            const textarea = document.getElementById('chat-textarea');
            if (textarea) textarea.style.height = 'auto';
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex flex-col h-[400px] w-full lg:w-80 bg-white/80 backdrop-blur-md rounded-2xl border border-white/20 shadow-xl overflow-hidden">
            <div className="p-4 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border-b border-white/10">
                <h3 className="font-bold text-gray-800 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                    Live Chat
                </h3>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar">
                {messages.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-gray-400 text-sm italic">
                        <p>Gửi lời chào để bắt đầu chat...</p>
                    </div>
                ) : (
                    messages.map((msg, index) => {
                        const isMe = msg.senderId === currentUserId;
                        return (
                            <div
                                key={index}
                                className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}
                            >
                                <div
                                    className={`max-w-[85%] rounded-2xl px-3 py-2 text-sm break-words shadow-sm ${isMe
                                            ? 'bg-indigo-500 text-white rounded-br-none'
                                            : 'bg-white text-gray-700 border border-gray-100 rounded-bl-none'
                                        }`}
                                >
                                    <p>{msg.message}</p>
                                </div>
                                <span className="text-[10px] text-gray-400 mt-1 px-1">
                                    {isMe ? 'You' : msg.sender} • {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                            </div>
                        );
                    })
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="p-3 bg-white/50 border-t border-white/10">
                <div className="flex gap-2 items-end bg-white rounded-xl border border-gray-200 p-2 focus-within:border-indigo-400 focus-within:ring-2 focus-within:ring-indigo-100 transition-all">
                    <textarea
                        id="chat-textarea"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder={disabled ? "Chat disabled" : "Type a message..."}
                        disabled={disabled}
                        maxLength={200}
                        className="flex-1 bg-transparent border-none focus:ring-0 p-1 text-sm resize-none max-h-20 min-h-[24px] outline-none text-gray-700 placeholder-gray-400 disabled:opacity-50"
                        rows={1}
                        style={{ height: 'auto', minHeight: '24px' }}
                        onInput={(e) => {
                            const target = e.target as HTMLTextAreaElement;
                            target.style.height = 'auto';
                            target.style.height = `${Math.min(target.scrollHeight, 80)}px`;
                        }}
                    />
                    <button
                        onClick={handleSend}
                        disabled={!newMessage.trim() || disabled}
                        className="p-2 rounded-lg bg-indigo-500 text-white hover:bg-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shrink-0"
                    >
                        <Send size={16} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatBox;
