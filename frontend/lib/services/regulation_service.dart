import 'package:flutter/foundation.dart';
import 'api_service.dart';

class Regulation {
  final String id;
  final String title;
  final String content;
  final List<String> clauses;

  Regulation({
    required this.id,
    required this.title,
    required this.content,
    required this.clauses,
  });

  factory Regulation.fromJson(Map<String, dynamic> json) {
    return Regulation(
      id: json['id'] ?? '',
      title: json['title'] ?? 'Unknown Regulation',
      content: json['content'] ?? '',
      clauses: (json['clauses'] as List?)?.cast<String>() ?? [],
    );
  }
}

class RegulationService extends ChangeNotifier {
  List<Regulation> _regulations = [];
  bool _isLoading = false;
  String? _error;
  String? _authToken;

  List<Regulation> get regulations => _regulations;
  bool get isLoading => _isLoading;
  String? get error => _error;

  RegulationService({String? authToken}) {
    _authToken = authToken;
  }

  void setAuth(String authToken) {
    _authToken = authToken;
  }

  Future<Map<String, dynamic>> queryRegulations(String query) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await ApiService.queryRegulations(
        query,
        authToken: _authToken,
      );

      if (response['success'] as bool) {
        final data = response['data'] as Map<String, dynamic>;
        
        if (data['regulations'] != null) {
          _regulations = (data['regulations'] as List)
              .map((r) => Regulation.fromJson(r as Map<String, dynamic>))
              .toList();
        }

        _isLoading = false;
        notifyListeners();
        return {'success': true, 'data': data};
      } else {
        _error = response['error']?.toString() ?? 'Failed to query regulations';
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

  Future<Map<String, dynamic>> getRegulationClauses(String regulationId) async {
    try {
      final response = await ApiService.getRegulationClauses(
        regulationId,
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

  Future<Map<String, dynamic>> validateAnswer(
    String answer,
    Map<String, dynamic> regulation,
  ) async {
    try {
      final response = await ApiService.validateAnswer(
        answer,
        regulation,
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

  Regulation? getRegulationById(String regulationId) {
    try {
      return _regulations.firstWhere((r) => r.id == regulationId);
    } catch (e) {
      return null;
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
