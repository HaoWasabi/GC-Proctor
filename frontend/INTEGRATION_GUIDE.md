# GC-Proctor Frontend - Backend Integration Guide

## ✅ Completed Integrations

### 1. **Exam & Rules Screen** (`/exam-rules`)
- **Backend Endpoints Used**:
  - `GET /api/exams` - Load all exams
  - `POST /api/chat/ask` - Ask questions about exams/rules
  - `POST /api/regulations/query` - Query regulations
  - `GET /api/regulations/{id}/clauses` - Get regulation details
  
- **Features**:
  - View upcoming exams in sidebar
  - Chat interface to ask about exams and regulations
  - Quick action buttons for common questions

### 2. **Study Screen** (`/study`)
- **Backend Endpoints Used**:
  - `POST /api/study/ask` - Ask study questions
  - `POST /api/study/flashcards/generate` - Generate flashcards
  - `POST /api/study/material/summarize` - Summarize materials
  - `POST /api/documents` - Upload study documents
  - `GET /api/documents` - List uploaded documents

- **Features**:
  - Upload and manage study materials
  - Ask questions about study materials
  - Generate flashcards for exam prep
  - Summarize course materials

### 3. **Admin Screen** (`/admin`)
- **Backend Endpoints Used**:
  - `GET /api/exams` - Display exam data for management
  - `POST /api/documents` - Upload documents
  - `DELETE /api/documents/{id}` - Delete documents (when implemented)

- **Features**:
  - View and manage exam database
  - Upload/import new files into knowledge base
  - Delete/edit file management

### 4. **Chat Integration (All Screens)**
- **Backend Endpoints Used**:
  - `POST /api/chat/ask` - Core chat functionality
  - `POST /api/chat/sessions/{id}/end` - End chat sessions
  - `GET /api/chat/sessions/{id}/context` - Get session context

- **Features**:
  - Persistent chat messages with UI
  - Loading states and error handling
  - Session management
  - Real-time responses from backend

## 🔧 Configuration

### Backend URL
Edit [api_service.dart](lib/services/api_service.dart):
```dart
static const String baseUrl = 'http://localhost:8000';
```

Change `localhost:8000` to your backend server address if needed.

### Student ID
Edit [main.dart](lib/main.dart) in the `ClassGeminiApp` widget:
```dart
ChatService(studentId: 'SV001'),
StudyService(studentId: 'SV001'),
```

## 📋 Available Services

### 1. **ChatService** - Core chat functionality
```dart
final chatService = context.read<ChatService>();
await chatService.sendMessage("Your question");
chatService.clearMessages();
```

### 2. **ExamService** - Exam management
```dart
final examService = context.read<ExamService>();
await examService.loadExams();
List<ExamData> upcomingExams = examService.getUpcomingExams();
```

### 3. **StudyService** - Study materials & questions
```dart
final studyService = context.read<StudyService>();
await studyService.askQuestion("Study question");
await studyService.generateFlashcards("courseId");
await studyService.uploadDocument("filePath");
```

### 4. **RegulationService** - Regulations & rules
```dart
final regService = context.read<RegulationService>();
final result = await regService.queryRegulations("query text");
```

### 5. **ApiService** - Low-level API calls
All HTTP requests to backend endpoints are handled here.

## 🚀 Running the Frontend

### Prerequisites
- Flutter SDK (latest version)
- Dart SDK
- Backend server running on configured URL

### Steps
1. **Install dependencies**:
   ```bash
   flutter pub get
   ```

2. **Run the app**:
   ```bash
   flutter run
   ```

3. **Build for web** (if needed):
   ```bash
   flutter build web
   ```

## 🧪 Testing Flows

### Test Exam Flow
1. Navigate to "Lịch Thi & Quy Chế"
2. Click on an exam in sidebar or ask "Lịch thi của tôi là gì?"
3. Verify exam data appears in chat

### Test Study Flow
1. Navigate to "Ôn Tập (Notebook)"
2. Ask a study question or request flashcards
3. Verify backend responds appropriately

### Test Admin Flow
1. Navigate to "Trang Quản Trị"
2. Verify exam list loads from backend
3. Test document upload functionality

## 📱 Screen Layout

### Desktop Layout
All screens use responsive design:
- **Desktop** (>800px width): Side panel + main content
- **Mobile** (<800px width): Drawer navigation + main content

### Screens
1. **Home** - Navigation cards to other screens
2. **Exam & Rules** - Chat-based exam information
3. **Study** - Document management + Q&A
4. **Admin** - Database management

## 🔄 Data Models

### ExamData
```dart
ExamData(
  id: 'exam_001',
  name: 'Midterm Exam',
  courseId: 'cs101',
  examDate: DateTime.now().add(Duration(days: 7)),
  location: 'Room 101',
  duration: 90, // minutes
)
```

### Flashcard
```dart
Flashcard(
  question: 'What is Flutter?',
  answer: 'Flutter is a UI framework...',
  level: 'medium' // easy, medium, hard
)
```

### Regulation
```dart
Regulation(
  id: 'reg_001',
  title: 'Attendance Policy',
  content: 'Students must...',
  clauses: ['clause1', 'clause2']
)
```

## 🐛 Debugging

### Enable verbose logging
Uncomment debug prints in services for development.

### Common Issues

**Connection timeout**
- Check backend is running on configured URL
- Verify firewall/network settings

**Empty data**
- Ensure backend has data in database
- Check API endpoints are correct
- Verify authentication tokens if needed

**UI not updating**
- Verify `notifyListeners()` is called in services
- Check `Consumer` widgets are properly wrapped
- May need `Future.microtask()` for timing issues

## 📚 Additional Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Provider Package](https://pub.dev/packages/provider)
- [HTTP Package](https://pub.dev/packages/http)
- [Backend API Docs](../doc/API_CONTRACT_P0.md)

## 🎯 Next Steps

- [ ] Implement document picker for file uploads
- [ ] Add flashcard UI with flip animation
- [ ] Implement regulation validation feature
- [ ] Add user authentication/login
- [ ] Implement offline mode
- [ ] Add performance optimization (caching)
- [ ] Add accessibility features
