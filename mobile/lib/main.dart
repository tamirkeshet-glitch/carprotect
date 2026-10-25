import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const CarProtectApp());
}

class CarProtectApp extends StatelessWidget {
  const CarProtectApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CarProtect',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue.shade800),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _controller = TextEditingController();
  bool _loading = false;
  String? _error;

  // שנה את הכתובת לפי היכן שהבקאנד רץ
  static const String apiBase = 'http://10.0.2.2:8000'; // Android emulator
  // static const String apiBase = 'http://localhost:8000'; // iOS simulator

  Future<void> _search() async {
    final plate = _controller.text.replaceAll(RegExp(r'\D'), '');
    if (plate.length < 5) {
      setState(() => _error = 'הכנס מספר רכב תקין');
      return;
    }

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final res = await http.get(Uri.parse('$apiBase/vehicle/$plate'));
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        if (!mounted) return;
        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => ReportScreen(data: data)),
        );
      } else {
        setState(() => _error = 'הרכב לא נמצא');
      }
    } catch (e) {
      setState(() => _error = 'לא ניתן להתחבר לשרת');
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('CarProtect'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const SizedBox(height: 40),
            const Text(
              'בדיקת רכב',
              style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              'ממקורות פתוחים • data.gov.il',
              style: TextStyle(color: Colors.grey.shade600),
            ),
            const SizedBox(height: 40),
            TextField(
              controller: _controller,
              keyboardType: TextInputType.number,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 24, letterSpacing: 4),
              decoration: InputDecoration(
                hintText: 'מספר רכב',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                contentPadding: const EdgeInsets.symmetric(vertical: 16),
              ),
              onSubmitted: (_) => _search(),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: FilledButton(
                onPressed: _loading ? null : _search,
                child: _loading
                    ? const SizedBox(width: 24, height: 24, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Text('בדוק', style: TextStyle(fontSize: 18)),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 16),
              Text(_error!, style: const TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

class ReportScreen extends StatelessWidget {
  final Map<String, dynamic> data;
  const ReportScreen({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final basic = data['basic'] as Map<String, dynamic>? ?? {};
    final mileage = data['mileage'] as Map<String, dynamic>? ?? {};
    final ownership = (data['ownership_history'] as List?) ?? [];
    final flags = (data['flags'] as List?) ?? [];
    final km = mileage['last_km'];

    return Scaffold(
      appBar: AppBar(title: Text('${basic['manufacturer'] ?? ''} ${basic['model'] ?? ''}')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _card('פרטים', [
            _row('יצרן', basic['manufacturer']),
            _row('דגם', basic['model']),
            _row('שנה', basic['year']?.toString()),
            _row('צבע', basic['color']),
            _row('דלק', basic['fuel']),
            _row('בעלות נוכחית', basic['current_ownership']),
          ]),
          _card('סטטוס', [
            _row('סטטוס', data['status']),
            _row('טסט אחרון', basic['last_test']),
            _row('תוקף רישיון', basic['license_expiry']),
            _row('ק"מ אחרון', km != null ? km.toString() : '-'),
          ]),
          if (ownership.isNotEmpty)
            _card('היסטוריית בעלויות', ownership.map<Widget>((o) {
              final m = o as Map;
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Text('${m['date']} — ${m['type']}'),
              );
            }).toList()),
          _card('דגלים', flags.isEmpty
              ? [const Text('אין דגלים מיוחדים', style: TextStyle(color: Colors.green))]
              : flags.map<Widget>((f) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2),
                    child: Text(f.toString(), style: const TextStyle(color: Colors.orange)),
                  )).toList()),
        ],
      ),
    );
  }

  Widget _card(String title, List<Widget> children) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _row(String label, String? value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: TextStyle(color: Colors.grey.shade600)),
          Text(value ?? '-', style: const TextStyle(fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
