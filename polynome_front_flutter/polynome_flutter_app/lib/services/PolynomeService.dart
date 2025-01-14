import 'dart:convert';
import 'package:http/http.dart' as http;

class BaseService {
  final String baseUrl = 'http://10.0.2.2:8081'; 

  Future<http.Response> getRequest(String endpoint) async {
    final response = await http.get(Uri.parse('$baseUrl$endpoint'));
    _handleResponse(response);
    return response;
  }

  Future<http.Response> postRequest(String endpoint, dynamic body, {bool isJson = true}) async {
    final headers = isJson ? {'Content-Type': 'application/json'} : {'Content-Type': 'application/x-www-form-urlencoded'};
    final encodedBody = isJson ? json.encode(body) : body;

    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: headers,
      body: encodedBody,
    );

    _handleResponse(response);
    return response;
  }

  void _handleResponse(http.Response response) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception('HTTP Error: ${response.statusCode}, Message: ${response.body}');
    }
  }
}

class PolynomeService extends BaseService {
  Future<List<dynamic>> getAllPolynomes() async {
    final response = await getRequest('/polynomes/all');
    return json.decode(response.body);
  }

  Future<void> savePolynome(Map<String, dynamic> data) async {
    await postRequest('/polynomes/save', data);
  }
}

class RacineService extends BaseService {
  Future<String> calculateRoots(String expression) async {
    final formattedExpression = expression.replaceAll(RegExp(r'\s+'), '');
    final response = await postRequest(
      '/racines/calculer',
      {'expression': formattedExpression},
    );
    return response.body;
  }
}

class FactorisationService extends BaseService {
  Future<String> factorize(String polynome) async {
    final formattedPolynome = polynome.replaceAll('^', '%5E');
    final encodedBody = 'polynome=$formattedPolynome';
    final response = await postRequest(
      '/api/factorisation/factorize',
      encodedBody,
      isJson: false,
    );
    return response.body;
  }
}
