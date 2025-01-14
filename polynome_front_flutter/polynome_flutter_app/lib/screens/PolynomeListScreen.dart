import 'package:flutter/material.dart';
import '../services/PolynomeService.dart';
import 'SavePolynomeScreen.dart';


class PolynomeListScreen extends StatefulWidget {
  @override
  _PolynomeListScreenState createState() => _PolynomeListScreenState();
}

class _PolynomeListScreenState extends State<PolynomeListScreen> {
  final PolynomeService service = PolynomeService();
  final RacineService racineService = RacineService();
  final FactorisationService factorisationService = FactorisationService();
  late Future<List> _polynomesFuture;

  @override
  void initState() {
    super.initState();
    _polynomesFuture = service.getAllPolynomes();
  }

  void _refreshPolynomes() {
    setState(() {
      _polynomesFuture = service.getAllPolynomes();
    });
  }

void _calculateRoots(String expression) async {
  try {
    final result = await racineService.calculateRoots(expression);
    _showResultDialog("Racines: $result");
  } catch (e) {
    _showErrorDialog("Error calculating roots: ${e.toString()}");
  }
}

  void _factorizePolynome(String expression) async {
    try {
      final result = await factorisationService.factorize(expression);
      _showResultDialog("Factorization: $result");
    } catch (e) {
      _showErrorDialog(e.toString());
    }
  }

  void _showResultDialog(String result) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Result'),
          content: Text(result),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Close'),
            ),
          ],
        );
      },
    );
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Error'),
          content: Text(message),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Close'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Polynomes'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => SavePolynomeScreen(refreshPolynomes: _refreshPolynomes),
                ),
              );
            },
          ),
        ],
      ),
      body: FutureBuilder<List>(
        future: _polynomesFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else {
            final polynomes = snapshot.data!;
            return ListView.builder(
              itemCount: polynomes.length,
              itemBuilder: (context, index) {
                final polynome = polynomes[index];
                return ListTile(
                  title: Text(polynome['expression']),
                  subtitle: Text(polynome['description'] ?? ''),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: Icon(Icons.calculate),
                        onPressed: () {
                          _calculateRoots(polynome['expression']);
                        },
                      ),
                      IconButton(
                        icon: Icon(Icons.extension),
                        onPressed: () {
                          _factorizePolynome(polynome['expression']);
                        },
                      ),
                    ],
                  ),
                );
              },
            );
          }
        },
      ),
    );
  }
}
