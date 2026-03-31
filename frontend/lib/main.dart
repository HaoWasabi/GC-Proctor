import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/chat_service.dart';
import 'services/exam_service.dart';
import 'services/study_service.dart';
import 'services/regulation_service.dart';

void main() {
  runApp(const ClassGeminiApp());
}

class ClassGeminiApp extends StatelessWidget {
  const ClassGeminiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => ChatService(
            studentId: 'SV001', 
          ),
        ),
        ChangeNotifierProvider(
          create: (_) => ExamService(),
        ),
        ChangeNotifierProvider(
          create: (_) => StudyService(studentId: 'SV001'),
        ),
        ChangeNotifierProvider(
          create: (_) => RegulationService(),
        ),
      ],
      child: MaterialApp(
        title: 'Class AI Assistant',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorSchemeSeed: Colors.blueAccent,
          brightness: Brightness.light,
          appBarTheme: AppBarTheme(
            backgroundColor: Colors.white,
            elevation: 0,
            iconTheme: IconThemeData(color: Colors.blue[900]),
            titleTextStyle: TextStyle(
              color: Colors.blue[900],
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        // Điểm bắt đầu là màn hình Home
        home: const HomeScreen(),
      ),
    );
  }
}

// ==========================================
// 1. MÀN HÌNH CHÍNH (HOME SCREEN)
// ==========================================
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text("Class AI - Trang Chủ"),
        centerTitle: true,
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 800),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  "Xin chào SV001! 👋\nBạn muốn làm gì hôm nay?",
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 40),
                Wrap(
                  spacing: 20,
                  runSpacing: 20,
                  alignment: WrapAlignment.center,
                  children: [
                    _buildNavCard(
                      context,
                      title: "Lịch Thi & Quy Chế",
                      icon: Icons.rule_folder,
                      color: Colors.blue,
                      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ExamAndRuleScreen())),
                    ),
                    _buildNavCard(
                      context,
                      title: "Ôn Tập (Notebook)",
                      icon: Icons.menu_book,
                      color: Colors.green,
                      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const StudyScreen())),
                    ),
                    _buildNavCard(
                      context,
                      title: "Trang Quản Trị (Admin)",
                      icon: Icons.admin_panel_settings,
                      color: Colors.orange,
                      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AdminScreen())),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildNavCard(BuildContext context, {required String title, required IconData icon, required Color color, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: 220,
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4)),
          ],
          border: Border.all(color: color.withOpacity(0.3), width: 2),
        ),
        child: Column(
          children: [
            Icon(icon, size: 64, color: color),
            const SizedBox(height: 16),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================
// 2. MÀN HÌNH LỊCH THI & QUY CHẾ (Giữ nguyên concept cũ)
// ==========================================
class ExamAndRuleScreen extends StatefulWidget {
  const ExamAndRuleScreen({super.key});

  @override
  State<ExamAndRuleScreen> createState() => _ExamAndRuleScreenState();
}

class _ExamAndRuleScreenState extends State<ExamAndRuleScreen> {
  final TextEditingController _messageController = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Load exams and regulations when screen opens
    Future.microtask(() {
      context.read<ExamService>().loadExams();
    });
  }

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final bool isDesktop = MediaQuery.of(context).size.width > 800;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Lịch thi & Quy chế"),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              context.read<ChatService>().clearMessages();
              context.read<ExamService>().loadExams();
            },
          ),
        ],
      ),
      drawer: isDesktop ? null : const ChatSidebar(),
      body: Row(
        children: [
          if (isDesktop) const SizedBox(width: 280, child: ChatSidebar()),
          if (isDesktop) const VerticalDivider(width: 1),
          Expanded(
            child: Column(
              children: [
                const ChatHeader(title: "Trợ lý Lịch thi & Quy chế"),
                Expanded(child: ChatArea()),
                MessageInput(controller: _messageController, onSend: () => _sendMessage(context, _messageController)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ==========================================
// 3. MÀN HÌNH ÔN TẬP (Giống LLM Notebook)
// ==========================================
class StudyScreen extends StatefulWidget {
  const StudyScreen({super.key});

  @override
  State<StudyScreen> createState() => _StudyScreenState();
}

class _StudyScreenState extends State<StudyScreen> {
  final TextEditingController _messageController = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Load study materials when screen opens
    Future.microtask(() {
      context.read<StudyService>().loadedMaterials;
    });
  }

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final bool isDesktop = MediaQuery.of(context).size.width > 800;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Không gian Ôn tập (Notebook)"),
      ),
      drawer: isDesktop ? null : Drawer(child: _buildSourcePanel()),
      body: Row(
        children: [
          if (isDesktop) 
            SizedBox(
              width: 300,
              child: _buildSourcePanel(), // Panel chứa tài liệu nguồn bên trái
            ),
          if (isDesktop) const VerticalDivider(width: 1),
          Expanded(
            child: Column(
              children: [
                const ChatHeader(title: "Hỏi đáp với Tài liệu ôn tập"),
                Expanded(child: ChatArea()),
                MessageInput(controller: _messageController, onSend: () => _sendStudyMessage(context, _messageController)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _sendStudyMessage(BuildContext context, TextEditingController controller) {
    if (controller.text.isNotEmpty) {
      final message = controller.text;
      controller.clear();
      context.read<StudyService>().askQuestion(message).then((result) {
        if (result['success'] as bool) {
          final chatService = context.read<ChatService>();
          final data = result['data'] as Map<String, dynamic>;
          final response = data['response'] ?? data['answer'] ?? 'Không có phản hồi';
          chatService.addInitialMessage(response);
        }
      });
    }
  }

  // Giao diện quản lý Nguồn tài liệu (Giống NotebookLM)
  Widget _buildSourcePanel() {
    return Container(
      color: Colors.grey[50],
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: ElevatedButton.icon(
              onPressed: () async {
                // TODO: Implement file picker
                // For now, show a snackbar
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Upload document feature coming soon")),
                );
              },
              icon: const Icon(Icons.upload_file),
              label: const Text("Tải tài liệu lên"),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: Colors.blue[600],
                foregroundColor: Colors.white,
              ),
            ),
          ),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: Text("NGUỒN TÀI LIỆU CỦA BẠN", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: Colors.grey)),
          ),
          Expanded(
            child: Consumer<StudyService>(
              builder: (context, studyService, _) {
                if (studyService.loadedMaterials.isEmpty) {
                  return Center(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Text(
                        "Chưa có tài liệu nào. Tải lên tài liệu để bắt đầu ôn tập!",
                        textAlign: TextAlign.center,
                        style: TextStyle(color: Colors.grey[500], fontSize: 13),
                      ),
                    ),
                  );
                }
                return ListView(
                  padding: const EdgeInsets.symmetric(horizontal: 8.0),
                  children: studyService.loadedMaterials
                      .map((material) => _buildSourceItem(material))
                      .toList(),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSourceItem(String filename) {
    return Card(
      elevation: 0,
      margin: const EdgeInsets.symmetric(vertical: 4),
      shape: RoundedRectangleBorder(
        side: BorderSide(color: Colors.grey[300]!),
        borderRadius: BorderRadius.circular(8),
      ),
      child: ListTile(
        leading: const Icon(Icons.description, color: Colors.blueAccent),
        title: Text(filename, style: const TextStyle(fontSize: 13), maxLines: 1, overflow: TextOverflow.ellipsis),
        trailing: const Icon(Icons.check_circle, color: Colors.green, size: 16),
      ),
    );
  }
}

// ==========================================
// 4. TRANG ADMIN (Quản lý File)
// ==========================================
class AdminScreen extends StatefulWidget {
  const AdminScreen({super.key});

  @override
  State<AdminScreen> createState() => _AdminScreenState();
}

class _AdminScreenState extends State<AdminScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      context.read<ExamService>().loadExams();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Quản trị hệ thống"),
        backgroundColor: Colors.orange[50],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "Quản lý Cơ sở dữ liệu AI",
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                ElevatedButton.icon(
                  onPressed: () {
                    // TODO: Mở dialog import file
                    ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Đang mở hộp thoại thêm file...")));
                  },
                  icon: const Icon(Icons.add),
                  label: const Text("Import File Mới"),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.orange,
                    foregroundColor: Colors.white,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            Expanded(
              child: Consumer<ExamService>(
                builder: (context, examService, _) {
                  if (examService.isLoading) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  
                  if (examService.exams.isEmpty) {
                    return Center(
                      child: Text(
                        "Chưa có dữ liệu để quản lý",
                        style: TextStyle(color: Colors.grey[500]),
                      ),
                    );
                  }

                  return ListView.builder(
                    itemCount: examService.exams.length,
                    itemBuilder: (context, index) {
                      final exam = examService.exams[index];
                      return _buildAdminFileTile(
                        context,
                        "${exam.name}.pdf",
                        "Lịch thi",
                        "1.2 MB",
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAdminFileTile(BuildContext context, String filename, String category, String size) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: Colors.orange[100],
          child: Icon(Icons.file_present, color: Colors.orange[800]),
        ),
        title: Text(filename, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text("Phân loại: $category • Kích thước: $size"),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            IconButton(
              icon: const Icon(Icons.edit, color: Colors.blue),
              onPressed: () {
                // TODO: Logic sửa
              },
              tooltip: "Sửa",
            ),
            IconButton(
              icon: const Icon(Icons.delete, color: Colors.red),
              onPressed: () {
                // TODO: Logic xóa
              },
              tooltip: "Xóa",
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================
// CÁC WIDGET DÙNG CHUNG (Tái sử dụng code cũ)
// ==========================================

void _sendMessage(BuildContext context, TextEditingController controller) {
  if (controller.text.isNotEmpty) {
    final message = controller.text;
    controller.clear();
    context.read<ChatService>().sendMessage(message);
  }
}

class ChatArea extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<ChatService>(
      builder: (context, chatService, _) {
        if (chatService.messages.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.chat_bubble_outline, size: 64, color: Colors.grey[300]),
                const SizedBox(height: 16),
                Text('Chưa có tin nhắn nào. Bắt đầu ngay!',
                    style: TextStyle(fontSize: 16, color: Colors.grey[500])),
              ],
            ),
          );
        }
        return ChatView(messages: chatService.messages);
      },
    );
  }
}

class ChatSidebar extends StatefulWidget {
  const ChatSidebar({super.key});

  @override
  State<ChatSidebar> createState() => _ChatSidebarState();
}

class _ChatSidebarState extends State<ChatSidebar> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      context.read<ExamService>().loadExams();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.grey[50],
      child: Column(
        children: [
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: ElevatedButton.icon(
                onPressed: () {
                  context.read<ChatService>().clearMessages();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Đã bắt đầu cuộc trò chuyện mới'), duration: Duration(seconds: 2)),
                  );
                },
                icon: const Icon(Icons.add),
                label: const Text("New Chat"),
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(double.infinity, 50),
                  backgroundColor: Colors.blue[100],
                  foregroundColor: Colors.blue[900],
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(12),
              children: [
                _buildSectionHeader("THÔNG TIN HỌC TẬP"),
                Consumer<ExamService>(
                  builder: (context, examService, _) {
                    final upcomingExams = examService.getUpcomingExams();
                    return Column(
                      children: upcomingExams.isNotEmpty
                          ? upcomingExams.take(2).map((exam) {
                              return _buildExamCard(
                                exam.name,
                                exam.examDate,
                                onTap: () => _insertExamMessage(context, exam),
                              );
                            }).toList()
                          : [
                              _buildFeatureCard(
                                "📅 Lịch Thi",
                                "Xem lịch thi sắp tới",
                                onTap: () => _insertMessage(context, "Lịch thi của tôi là gì?"),
                              ),
                            ],
                    );
                  },
                ),
                const SizedBox(height: 16),
                _buildSectionHeader("CÂU HỎI THƯỜNG GẶP"),
                _buildFeatureCard("📋 Quy Chế", "Quy chế điểm danh", onTap: () => _insertMessage(context, "Quy chế về điểm danh như thế nào?")),
                _buildFeatureCard("🎓 Ôn Tập", "Tạo Flashcard", onTap: () => _generateFlashcards(context)),
                _buildFeatureCard("📚 Tài Liệu", "Tóm tắt tài liệu", onTap: () => _insertMessage(context, "Tóm tắt tài liệu chính khóa cho tôi")),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildExamCard(String title, DateTime examDate, {required VoidCallback onTap}) {
    final dateStr = "${examDate.day}/${examDate.month}/${examDate.year}";
    return Card(
      elevation: 0,
      color: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: BorderSide(color: Colors.blue[200]!)),
      child: ListTile(
        leading: Icon(Icons.event, color: Colors.blue[600]),
        title: Text(title, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold), maxLines: 1, overflow: TextOverflow.ellipsis),
        subtitle: Text(dateStr, style: const TextStyle(fontSize: 11)),
        onTap: onTap,
      ),
    );
  }

  void _insertExamMessage(BuildContext context, dynamic exam) {
    context.read<ChatService>().sendMessage("Cho tôi thông tin chi tiết về lịch thi ${exam.name}");
  }

  void _generateFlashcards(BuildContext context) {
    // TODO: Implement course selection and flashcard generation
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Tạo Flashcard - chọn khóa học")),
    );
  }

  void _insertMessage(BuildContext context, String message) {
    context.read<ChatService>().sendMessage(message);
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 8, bottom: 8, top: 12),
      child: Text(title, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey[600])),
    );
  }

  Widget _buildFeatureCard(String title, String subtitle, {required VoidCallback onTap}) {
    return Card(
      elevation: 0,
      color: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: BorderSide(color: Colors.grey[200]!)),
      child: ListTile(
        title: Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle, style: const TextStyle(fontSize: 12)),
        onTap: onTap,
      ),
    );
  }
}

class ChatHeader extends StatelessWidget {
  final String title;
  const ChatHeader({super.key, this.title = "AI Study Assistant"});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 4, offset: const Offset(0, 2))]),
      child: Row(
        children: [
          Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const Spacer(),
          IconButton(onPressed: () {}, icon: const Icon(Icons.search)),
          const CircleAvatar(backgroundImage: NetworkImage("https://api.dicebear.com/8.x/notionists/png?seed=John")),
        ],
      ),
    );
  }
}

class ChatView extends StatefulWidget {
  final List<dynamic> messages; // Dùng dynamic hoặc ChatMessage tùy file chat_service.dart của bạn
  const ChatView({super.key, required this.messages});

  @override
  State<ChatView> createState() => _ChatViewState();
}

class _ChatViewState extends State<ChatView> {
  late ScrollController _scrollController;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
  }

  @override
  void didUpdateWidget(ChatView oldWidget) {
    super.didUpdateWidget(oldWidget);
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: _scrollController,
      padding: const EdgeInsets.all(20),
      itemCount: widget.messages.length,
      itemBuilder: (context, index) {
        final message = widget.messages[index];
        final isUser = message.sender == 'user';
        return MessageBubble(
          text: message.text,
          isUser: isUser,
          isLoading: message.isLoading,
        );
      },
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }
}

class MessageBubble extends StatelessWidget {
  final String text;
  final bool isUser;
  final bool isLoading;

  const MessageBubble({super.key, required this.text, required this.isUser, this.isLoading = false});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!isUser) const CircleAvatar(child: Icon(Icons.bolt, color: Colors.white), backgroundColor: Colors.blueAccent, radius: 16),
          const SizedBox(width: 10),
          Flexible(
            child: Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: isUser ? Colors.blue[600] : Colors.grey[100],
                borderRadius: BorderRadius.only(
                  topLeft: const Radius.circular(16),
                  topRight: const Radius.circular(16),
                  bottomLeft: isUser ? const Radius.circular(16) : Radius.zero,
                  bottomRight: isUser ? Radius.zero : const Radius.circular(16),
                ),
              ),
              child: isLoading
                  ? Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, valueColor: AlwaysStoppedAnimation<Color>(Colors.grey[600]!))),
                        const SizedBox(width: 8),
                        Text(text, style: TextStyle(color: Colors.grey[600], fontSize: 14, fontStyle: FontStyle.italic)),
                      ],
                    )
                  : Text(text, style: TextStyle(color: isUser ? Colors.white : Colors.black87, fontSize: 14)),
            ),
          ),
          if (isUser) const SizedBox(width: 10),
          if (isUser) const CircleAvatar(backgroundImage: NetworkImage("https://api.dicebear.com/8.x/notionists/png?seed=John"), radius: 16),
        ],
      ),
    );
  }
}

class MessageInput extends StatelessWidget {
  final TextEditingController controller;
  final VoidCallback onSend;
  const MessageInput({super.key, required this.controller, required this.onSend});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(color: Colors.white, border: Border(top: BorderSide(color: Colors.grey[200]!))),
      child: Row(
        children: [
          IconButton(onPressed: () {}, icon: const Icon(Icons.add_circle_outline, color: Colors.blue)),
          Expanded(
            child: TextField(
              controller: controller,
              decoration: InputDecoration(
                hintText: "Nhập câu hỏi của bạn...",
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
                filled: true,
                fillColor: Colors.grey[100],
                contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              ),
              onSubmitted: (_) => onSend(),
            ),
          ),
          const SizedBox(width: 10),
          FloatingActionButton.small(onPressed: onSend, child: const Icon(Icons.send), backgroundColor: Colors.blue[600], foregroundColor: Colors.white, elevation: 2),
        ],
      ),
    );
  }
}