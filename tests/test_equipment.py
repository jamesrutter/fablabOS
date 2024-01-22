
def test_index(client):
    """Test listing all equipment."""
    response = client.get('/equipment/')
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert 'status' in response.json
    assert response.json['status'] == 'success'


def test_detail(client):
    """Test getting a single equipment detail."""
    # Assume an equipment with id=1 exists
    response = client.get('/equipment/1')
    assert response.status_code in [200, 404]


# TO DO: Add authentication headers fixture for testing authenticated endpoints
# def test_create(client, auth_headers):
#     """Test creating a new equipment item."""
#     # auth_headers is a fixture that provides authentication headers
#     response = client.post('/equipment/', headers=auth_headers, data={
#                            'name': 'New Equipment', 'description': 'Description of new equipment'})
#     assert response.status_code == 201
#     assert isinstance(response.json, dict)
#     assert response.json['status'] == 'success'


# def test_delete(client, auth_headers):
#     """Test deleting an equipment item."""
#     # Assume an equipment with id=1 exists
#     response = client.delete('/equipment/1', headers=auth_headers)
#     assert response.status_code in [204, 404]

# def test_update(client, auth_headers):
#     """Test updating an existing equipment item."""
#     # Assume an equipment with id=1 exists
#     response = client.put('/equipment/1', headers=auth_headers, data={'name': 'Updated Name', 'description': 'Updated Description'})
#     assert response.status_code in [200, 404]
