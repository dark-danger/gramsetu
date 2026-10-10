import 'package:flutter/material.dart';
import 'screens/home_chat_screen.dart';
import 'screens/kisan_screen.dart';
import 'screens/yojana_screen.dart';
import 'screens/swasthya_screen.dart';
import 'screens/calculator_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const GramSetuApp());
}

class GramSetuApp extends StatelessWidget {
  const GramSetuApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GramSetu AI (ग्रामसेतु AI)',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF090D16),
        primaryColor: const Color(0xFF15803D),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF15803D),
          secondary: Color(0xFFD97706),
          surface: Color(0xFF0F172A),
        ),
        fontFamily: 'Inter',
      ),
      home: const MainNavigationShell(),
    );
  }
}

class MainNavigationShell extends StatefulWidget {
  const MainNavigationShell({super.key});

  @override
  State<MainNavigationShell> createState() => _MainNavigationShellState();
}

class _MainNavigationShellState extends State<MainNavigationShell> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    HomeChatScreen(),
    KisanScreen(),
    YojanaScreen(),
    SwasthyaScreen(),
    CalculatorScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (idx) => setState(() => _currentIndex = idx),
        backgroundColor: const Color(0xFF0F172A),
        indicatorColor: const Color(0xFF15803D).withOpacity(0.3),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.chat_bubble_outline),
            selectedIcon: Icon(Icons.chat_bubble, color: Color(0xFF4ADE80)),
            label: 'AI सहायक',
          ),
          NavigationDestination(
            icon: Icon(Icons.agriculture_outlined),
            selectedIcon: Icon(Icons.agriculture, color: Color(0xFF4ADE80)),
            label: 'किसान',
          ),
          NavigationDestination(
            icon: Icon(Icons.account_balance_outlined),
            selectedIcon: Icon(Icons.account_balance, color: Color(0xFF4ADE80)),
            label: 'योजनाएं',
          ),
          NavigationDestination(
            icon: Icon(Icons.medical_services_outlined),
            selectedIcon: Icon(Icons.medical_services, color: Color(0xFFF87171)),
            label: 'स्वास्थ्य',
          ),
          NavigationDestination(
            icon: Icon(Icons.calculate_outlined),
            selectedIcon: Icon(Icons.calculate, color: Color(0xFFA78BFA)),
            label: 'नाप-तौल',
          ),
        ],
      ),
    );
  }
}
