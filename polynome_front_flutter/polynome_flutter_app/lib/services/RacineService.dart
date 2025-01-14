import 'package:flutter/material.dart';
import 'PolynomeService.dart';

class PolynomeListScreen extends StatelessWidget {
  final PolynomeService service = PolynomeService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Polynomes')),
      body: FutureBuilder<List>(
        future: service.getAllPolynomes(),
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
                );
              },
            );
          }
        },
      ),
    );
  }
}
