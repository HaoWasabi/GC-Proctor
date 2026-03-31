import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  static const String apiPrefix = '/api';

  // ============ CHAT ENDPOINTS ============
  static Future<Map<String, dynamic>> askChat(
    String question, {
    String? sessionId,
    String? studentId,
    String? authToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$apiPrefix/chat/ask'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
        body: jsonEncode({
          'query': question,
          'session_id': sessionId,
          'student_id': studentId,
        }),
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = jsonDecode(response.body);
        return {
          'success': true,
          'data': data['data'] ?? data,
        };
      } else {
        return {
          'success': false,
          'error': 'Server error: ${response.statusCode}',
        };
      }
    } catch (e) {
      return {
        'success': false,
        'error': 'Error: ${e.toString()}',
      };
    }
  }

  static Future<Map<String, dynamic>> endChatSession(
    String sessionId, {
    String? authToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$apiPrefix/chat/sessions/$sessionId/end'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
      ).timeout(
        const Duration(seconds: 15),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data['data'] ?? data};
      } else {
        return {'success': false, 'error': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  // ============ EXAM ENDPOINTS ============
  static Future<Map<String, dynamic>> getExams({String? authToken}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl$apiPrefix/exams'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
      ).timeout(
        const Duration(seconds: 15),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {
          'success': true,
          'data': data['data'] ?? data,
        };
      } else {
        return {
          'success': false,
          'error': 'Server error: ${response.statusCode}',
        };
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  static Future<Map<String, dynamic>> getExamById(
    String examId, {
    String? authToken,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl$apiPrefix/exams/$examId'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
      ).timeout(
        const Duration(seconds: 15),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data['data'] ?? data};
      } else {
        return {'success': false, 'error': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  // ============ REGULATION ENDPOINTS ============
  static Future<Map<String, dynamic>> queryRegulations(
    String query, {
    String? authToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$apiPrefix/regulations/query'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
        body: jsonEncode({'query': query}),
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {
          'success': true,
          'data': data['data'] ?? data,
        };
      } else {
        return {
          'success': false,
          'error': 'Server error: ${response.statusCode}',
        };
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  static Future<Map<String, dynamic>> getRegulationClauses(
    String regulationId, {
    String? authToken,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl$apiPrefix/regulations/$regulationId/clauses'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {
          'success': true,
          'data': data['data'] ?? data,
        };
      } else {
        return {
          'success': false,
          'error': 'Server error: ${response.statusCode}',
        };
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  static Future<Map<String, dynamic>> validateAnswer(
    String answer,
    Map<String, dynamic> regulation, {
    String? authToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$apiPrefix/regulations/validate-answer'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
        body: jsonEncode({'answer': answer, 'regulation': regulation}),
      ).timeout(
        const Duration(seconds: 15),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data['data'] ?? data};
      } else {
        return {'success': false, 'error': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  // ============ STUDY ENDPOINTS ============
  static Future<Map<String, dynamic>> askStudyQuestion(
    String question, {
    String? studentId,
    String? authToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$apiPrefix/study/ask'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
        body: jsonEncode({
          'query': question,
          'student_id': studentId,
        }),
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data['data'] ?? data};
      } else {
        return {'success': false, 'error': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  static Future<Map<String, dynamic>> generateFlashcards(
    String courseId, {
    String? studentId,
    String? authToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$apiPrefix/study/flashcards/generate'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
        body: jsonEncode({
          'course_id': courseId,
          'student_id': studentId,
        }),
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data['data'] ?? data};
      } else {
        return {'success': false, 'error': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  static Future<Map<String, dynamic>> summarizeMaterial(
    String courseId, {
    String? studentId,
    String? authToken,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$apiPrefix/study/material/summarize'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
        body: jsonEncode({
          'course_id': courseId,
          'student_id': studentId,
        }),
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data['data'] ?? data};
      } else {
        return {'success': false, 'error': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  // ============ DOCUMENT ENDPOINTS ============
  static Future<Map<String, dynamic>> getDocuments({String? authToken}) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl$apiPrefix/documents'),
        headers: {
          'Content-Type': 'application/json',
          if (authToken != null) 'Authorization': 'Bearer $authToken',
        },
      ).timeout(
        const Duration(seconds: 15),
        onTimeout: () => throw Exception('Request timeout'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data['data'] ?? data};
      } else {
        return {'success': false, 'error': 'Server error: ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }

  static Future<Map<String, dynamic>> uploadDocument(
    String filePath, {
    String? studentId,
    String? authToken,
  }) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl$apiPrefix/documents'),
      );

      request.files.add(await http.MultipartFile.fromPath('file', filePath));
      if (studentId != null) request.fields['student_id'] = studentId;
      if (authToken != null) request.headers['Authorization'] = 'Bearer $authToken';

      final response = await request.send().timeout(
        const Duration(seconds: 60),
        onTimeout: () => throw Exception('Upload timeout'),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final responseData = await response.stream.bytesToString();
        final data = jsonDecode(responseData);
        return {'success': true, 'data': data['data'] ?? data};
      } else {
        return {'success': false, 'error': 'Upload failed: ${response.statusCode}'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Error: ${e.toString()}'};
    }
  }
}

