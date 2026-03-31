import 'package:flutter/foundation.dart';
import 'api_service.dart';

class Flashcard {
  final String question;
  final String answer;
  final String level; // easy, medium, hard

  Flashcard({
    required this.question,
    required this.answer,
    required this.level,
  });

  factory Flashcard.fromJson(Map<String, dynamic> json) {
    return Flashcard(
      question: json['question'] ?? '',
      answer: json['answer'] ?? '',
      level: json['level'] ?? 'medium',
    );
  }
}

class StudyService extends ChangeNotifier {
  List<String> _loadedMaterials = [];
  List<Flashcard> _flashcards = [];
  bool _isLoading = false;
  String? _error;
  String? _studentId;
  String? _authToken;

  List<String> get loadedMaterials => _loadedMaterials;
  List<Flashcard> get flashcards => _flashcards;
  bool get isLoading => _isLoading;
  String? get error => _error;

  StudyService({String? studentId, String? authToken}) {
    _studentId = studentId;
    _authToken = authToken;
  }

  void setAuth(String studentId, String authToken) {
    _studentId = studentId;
    _authToken = authToken;
  }

  Future<Map<String, dynamic>> askQuestion(String question) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiService.askStudyQuestion(
        question,
        studentId: _studentId,
        authToken: _authToken,
      );

      if (response['success'] as bool) {
        final data = response['data'] as Map<String, dynamic>;
        _isLoading = false;
        notifyListeners();
        return {'success': true, 'data': data};
      } else {
        _error = response['error']?.toString() ?? 'Failed to ask question';
        _isLoading = false;
        notifyListeners();
        return {'success': false, 'error': _error};
      }
    } catch (e) {
      _error = 'Error: ${e.toString()}';
      _isLoading = false;
      notifyListeners();
      return {'success': false, 'error': _error};
    }
  }

  Future<void> generateFlashcards(String courseId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiService.generateFlashcards(
        courseId,
        studentId: _studentId,
        authToken: _authToken,
      );

      if (response['success'] as bool) {
        final data = response['data'] as Map<String, dynamic>;
        
        if (data['flashcards'] != null) {
          _flashcards = (data['flashcards'] as List)
              .map((f) => Flashcard.fromJson(f as Map<String, dynamic>))
              .toList();
        }
      } else {
        _error = response['error']?.toString() ?? 'Failed to generate flashcards';
      }
    } catch (e) {
      _error = 'Error: ${e.toString()}';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Map<String, dynamic>> summarizeMaterial(String courseId) async {
    try {
      final response = await ApiService.summarizeMaterial(
        courseId,
        studentId: _studentId,
        authToken: _authToken,
      );

      if (response['success'] as bool) {
        return {'success': true, 'data': response['data']};
      } else {
        return {'success': false, 'error': response['error']};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  Future<void> uploadDocument(String filePath) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiService.uploadDocument(
        filePath,
        studentId: _studentId,
        authToken: _authToken,
      );

      if (response['success'] as bool) {
        final data = response['data'] as Map<String, dynamic>;
        final fileName = data['filename'] ?? filePath.split('/').last;
        
        if (!_loadedMaterials.contains(fileName)) {
          _loadedMaterials.add(fileName);
        }
      } else {
        _error = response['error']?.toString() ?? 'Upload failed';
      }
    } catch (e) {
      _error = 'Error: ${e.toString()}';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
