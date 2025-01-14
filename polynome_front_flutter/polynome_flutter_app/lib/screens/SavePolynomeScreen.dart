import 'package:flutter/material.dart';
import '../services/PolynomeService.dart';

class SavePolynomeScreen extends StatefulWidget {
  final Function refreshPolynomes;

  SavePolynomeScreen({required this.refreshPolynomes});

  @override
  _SavePolynomeScreenState createState() => _SavePolynomeScreenState();
}

class _SavePolynomeScreenState extends State<SavePolynomeScreen> {
  final _formKey = GlobalKey<FormState>();
  final _expressionController = TextEditingController();
  final _descriptionController = TextEditingController();
  final PolynomeService service = PolynomeService();

  void _savePolynome() async {
    if (_formKey.currentState!.validate()) {
      try {
        await service.savePolynome({
          'expression': _expressionController.text,
          'description': _descriptionController.text,
        });
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text('Polynome saved successfully')));
        
        // Refresh the list of polynomes in the parent screen
        widget.refreshPolynomes();
        
        Navigator.pop(context);
      } catch (e) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text('Error: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Save Polynome')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _expressionController,
                decoration: InputDecoration(labelText: 'Expression'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter an expression';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _descriptionController,
                decoration: InputDecoration(labelText: 'Description'),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _savePolynome,
                child: Text('Save Polynome'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
