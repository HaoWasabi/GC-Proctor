import 'package:flutter/foundation.dart';
import 'api_service.dart';

class ExamData {
  final String id;
  final String name;
  final String courseId;
  final DateTime examDate;
  final String location;
  final int duration; // in minutes
  final String? description;

  ExamData({
    required this.id,
    required this.name,
    required this.courseId,
    required this.examDate,
    required this.location,
    required this.duration,
    this.description,
  });

  factory ExamData.fromJson(Map<String, dynamic> json) {
    return ExamData(
      id: json['id'] ?? '',
      name: json['name'] ?? 'Unknown Exam',
      courseId: json['course_id'] ?? '',
      examDate: DateTime.tryParse(json['exam_date'].toString()) ?? DateTime.now(),
      location: json['location'] ?? 'TBD',
      duration: json['duration'] ?? 0,
      description: json['description'],
    );
  }
}

class ExamService extends ChangeNotifier {
  List<ExamData> _exams = [];
  bool _isLoading = false;
  String? _error;
  String? _authToken;

  List<ExamData> get exams => _exams;
  bool get isLoading => _isLoading;
  String? get error => _error;

  ExamService({String? authToken}) {
    _authToken = authToken;
  }

  void setAuth(String authToken) {
    _authToken = authToken;
  }

  Future<void> loadExams() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiService.getExams(authToken: _authToken);

      if (response['success'] as bool) {
        final data = response['data'] as Map<String, dynamic>;
        
        if (data['exams'] != null) {
          _exams = (data['exams'] as List)
              .map((e) => ExamData.fromJson(e as Map<String, dynamic>))
              .toList();
        } else if (data is List) {
          _exams = (data as List)
              .map((e) => ExamData.fromJson(e as Map<String, dynamic>))
              .toList();
        }
      } else {
        _error = response['error']?.toString() ?? 'Failed to load exams';
      }
    } catch (e) {
      _error = 'Error: ${e.toString()}';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<ExamData?> getExamById(String examId) async {
    try {
      final response = await ApiService.getExamById(examId, authToken: _authToken);
      
      if (response['success'] as bool) {
        final data = response['data'] as Map<String, dynamic>;
        return ExamData.fromJson(data);
      }
      return null;
    } catch (e) {
      _error = 'Error: ${e.toString()}';
      return null;
    }
  }

  List<ExamData> getUpcomingExams() {
    final now = DateTime.now();
    return _exams.where((exam) => exam.examDate.isAfter(now)).toList()
      ..sort((a, b) => a.examDate.compareTo(b.examDate));
  }

  List<ExamData> getPastExams() {
    final now = DateTime.now();
    return _exams.where((exam) => exam.examDate.isBefore(now)).toList()
      ..sort((a, b) => b.examDate.compareTo(a.examDate));
  }

  clearError() {
    _error = null;
    notifyListeners();
  }
}
