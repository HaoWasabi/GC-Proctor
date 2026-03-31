import 'package:flutter/foundation.dart';
import 'api_service.dart';

class ChatMessage {
  final String id;
  final String sender; // 'user' or 'ai'
  final String text;
  final DateTime timestamp;
  final bool isLoading;

  ChatMessage({
    required this.id,
    required this.sender,
    required this.text,
    required this.timestamp,
    this.isLoading = false,
  });

  ChatMessage copyWith({
    String? id,
    String? sender,
    String? text,
    DateTime? timestamp,
    bool? isLoading,
  }) {
    return ChatMessage(
      id: id ?? this.id,
      sender: sender ?? this.sender,
      text: text ?? this.text,
      timestamp: timestamp ?? this.timestamp,
      isLoading: isLoading ?? this.isLoading,
    );
  }
}

class ChatService extends ChangeNotifier {
  List<ChatMessage> _messages = [];
  String? _sessionId;
  String? _studentId;
  String? _authToken;
  bool _isLoading = false;

  List<ChatMessage> get messages => _messages;
  bool get isLoading => _isLoading;
  String? get sessionId => _sessionId;

  ChatService({
    String? studentId,
    String? authToken,
  }) {
    _studentId = studentId;
    _authToken = authToken;
  }

  void setAuth(String studentId, String authToken) {
    _studentId = studentId;
    _authToken = authToken;
  }

  void addMessage(ChatMessage message) {
    _messages.add(message);
    notifyListeners();
  }

  void updateMessage(int index, ChatMessage message) {
    if (index >= 0 && index < _messages.length) {
      _messages[index] = message;
      notifyListeners();
    }
  }

  Future<void> sendMessage(String userQuery) async {
    // Thêm tin nhắn của user
    final userMessage = ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      sender: 'user',
      text: userQuery,
      timestamp: DateTime.now(),
    );
    addMessage(userMessage);

    // Thêm tin nhắn loading của AI
    final loadingIndex = _messages.length;
    final loadingMessage = ChatMessage(
      id: 'loading_${DateTime.now().millisecondsSinceEpoch}',
      sender: 'ai',
      text: 'Đang suy nghĩ...',
      timestamp: DateTime.now(),
      isLoading: true,
    );
    addMessage(loadingMessage);

    _isLoading = true;
    notifyListeners();

    try {
      // Gọi API chat
      final response = await ApiService.askChat(
        userQuery,
        sessionId: _sessionId,
        studentId: _studentId,
        authToken: _authToken,
      );

      if (response['success'] as bool) {
        // Lấy phản hồi từ backend
        final data = response['data'] as Map<String, dynamic>;
        String aiResponse = 'Xin lỗi, tôi không thể xử lý yêu cầu này.';

        if (data['response'] != null) {
          aiResponse = data['response'].toString();
        } else if (data['answer'] != null) {
          aiResponse = data['answer'].toString();
        }

        // Cập nhật session ID nếu có
        if (data['session_id'] != null) {
          _sessionId = data['session_id'].toString();
        }

        // Cập nhật tin nhắn loading thành tin nhắn AI thực
        final aiMessage = ChatMessage(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          sender: 'ai',
          text: aiResponse,
          timestamp: DateTime.now(),
        );

        // Xóa tin nhắn loading và thêm tin nhắn thực
        _messages.removeAt(loadingIndex);
        addMessage(aiMessage);
      } else {
        // Hiển thị lỗi
        final errorMessage = ChatMessage(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          sender: 'ai',
          text: 'Lỗi: ${response['error'] ?? 'Lỗi không xác định'}',
          timestamp: DateTime.now(),
        );

        _messages.removeAt(loadingIndex);
        addMessage(errorMessage);
      }
    } catch (e) {
      final errorMessage = ChatMessage(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        sender: 'ai',
        text: 'Lỗi kết nối: ${e.toString()}',
        timestamp: DateTime.now(),
      );

      _messages.removeAt(loadingIndex);
      addMessage(errorMessage);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearMessages() {
    _messages.clear();
    _sessionId = null;
    notifyListeners();
  }

  void addInitialMessage(String text) {
    final message = ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      sender: 'ai',
      text: text,
      timestamp: DateTime.now(),
    );
    addMessage(message);
  }
}
