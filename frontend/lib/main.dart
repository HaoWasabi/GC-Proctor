import 'package:flutter/material.dart';

void main() {
  runApp(const ClassGeminiApp());
}

class ClassGeminiApp extends StatelessWidget {
  const ClassGeminiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Class AI Assistant',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.blueAccent,
        brightness: Brightness.light,
      ),
      home: const MainChatScreen(),
    );
  }
}

class MainChatScreen extends StatefulWidget {
  const MainChatScreen({super.key});

  @override
  State<MainChatScreen> createState() => _MainChatScreenState();
}

class _MainChatScreenState extends State<MainChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final List<Map<String, String>> _messages = [
    {"sender": "user", "text": "Hello! Can you explain the theory of relativity?"},
    {"sender": "ai", "text": "Hello! Let's simplify it. It's about how things relate to each other in terms of space and time. A famous example is..."},
    {"sender": "ai", "text": "Think of a fabric stretched tight. That's space-time..."},
  ];

  @override
  Widget build(BuildContext context) {
    // Determine screen size for responsiveness
    final bool isDesktop = MediaQuery.of(context).size.width > 800;

    return Scaffold(
      appBar: isDesktop ? null : AppBar(title: const Text("Class AI")),
      drawer: isDesktop ? null : const ChatSidebar(), // Drawer for mobile
      body: Row(
        children: [
          if (isDesktop)
            const SizedBox(width: 280, child: ChatSidebar()), // Fixed sidebar for desktop
          const VerticalDivider(width: 1),
          Expanded(
            child: Column(
              children: [
                // Chat Header (Gemini Style)
                const ChatHeader(),
                // Chat Messages (Main View)
                Expanded(child: ChatView(messages: _messages)),
                // Message Input (Bottom)
                MessageInput(controller: _messageController, onSend: _sendMessage),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _sendMessage() {
    if (_messageController.text.isNotEmpty) {
      setState(() {
        _messages.add({"sender": "user", "text": _messageController.text});
        // Simulate an AI response after a delay
        Future.delayed(const Duration(seconds: 1), () {
          if(mounted) {
            setState(() {
              _messages.add({"sender": "ai", "text": "That's an interesting point. Let me analyze that in the context of our module."});
            });
          }
        });
        _messageController.clear();
      });
    }
  }
}

// --- SideBar Widget (Classroom Style) ---
class ChatSidebar extends StatelessWidget {
  const ChatSidebar({super.key});

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
                onPressed: () {},
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
                _buildSectionHeader("RECENT CONVERSATIONS"),
                _buildChatCard("Quantum Mechanics Intro", Icons.psychology),
                _buildChatCard("History Paper Outline", Icons.history_edu),
                const SizedBox(height: 20),
                _buildSectionHeader("MY CLASSES (Classroom Style)"),
                _buildClassCard("Physics 101", "Dr. Smith", Colors.orange),
                _buildClassCard("History of Art", "Prof. Jones", Colors.green),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 8, bottom: 8, top: 12),
      child: Text(title, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey[600])),
    );
  }

  Widget _buildChatCard(String title, IconData icon) {
    return Card(
      elevation: 0,
      color: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: BorderSide(color: Colors.grey[200]!)),
      child: ListTile(
        leading: Icon(icon, color: Colors.blue),
        title: Text(title, style: const TextStyle(fontSize: 14)),
        onTap: () {},
      ),
    );
  }

  Widget _buildClassCard(String title, String instructor, Color color) {
    return Card(
      elevation: 0,
      color: color.withValues(alpha: 0.1),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: BorderSide(color: color.withValues(alpha: 0.2))),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: color, child: const Icon(Icons.class_, color: Colors.white)),
        title: Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
        subtitle: Text(instructor, style: const TextStyle(fontSize: 12)),
        onTap: () {},
      ),
    );
  }
}

// --- Chat Header Widget ---
class ChatHeader extends StatelessWidget {
  const ChatHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 4, offset: const Offset(0, 2))]),
      child: Row(
        children: [
          const Text("AI Study Assistant", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const Spacer(),
          IconButton(onPressed: () {}, icon: const Icon(Icons.search)),
          const CircleAvatar(backgroundImage: NetworkImage("https://api.dicebear.com/8.x/notionists/png?seed=John")),
        ],
      ),
    );
  }
}

// --- Main Chat View Widget ---
class ChatView extends StatelessWidget {
  final List<Map<String, String>> messages;
  const ChatView({super.key, required this.messages});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(20),
      itemCount: messages.length,
      itemBuilder: (context, index) {
        final message = messages[index];
        final isUser = message["sender"] == "user";
        return MessageBubble(text: message["text"]!, isUser: isUser);
      },
    );
  }
}

// --- Message Bubble Widget ---
class MessageBubble extends StatelessWidget {
  final String text;
  final bool isUser;
  const MessageBubble({super.key, required this.text, required this.isUser});

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
              child: Text(text, style: TextStyle(color: isUser ? Colors.white : Colors.black87, fontSize: 14)),
            ),
          ),
          if (isUser) const SizedBox(width: 10),
          if (isUser) const CircleAvatar(backgroundImage: NetworkImage("https://api.dicebear.com/8.x/notionists/png?seed=John"), radius: 16),
        ],
      ),
    );
  }
}

// --- Message Input Widget ---
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
                hintText: "Ask anything about your module...",
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