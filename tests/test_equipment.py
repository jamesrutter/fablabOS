
def test_get_equipment_list_success(client):
    """Test listing all equipment."""
    response = client.get('/equipment/')
    assert response.status_code == 200
    json_data = response.json

    assert isinstance(json_data, dict)
    assert 'status' in json_data
    assert json_data['status'] == 'success'
    assert 'data' in json_data
    # return data should be a list of dictionaries
    assert isinstance(json_data['data'], list)

    assert len(json_data['data']) > 0
    assert 'name' in json_data['data'][0]
    assert 'description' in json_data['data'][0]


def test_get_equipment_detail_success(client):
    """Test getting a single equipment detail successfully."""
    # Assume an equipment with id=1 exists
    response = client.get('/equipment/1')
    assert response.status_code == 200
    json_data = response.json

    assert isinstance(json_data, dict)
    assert 'status' in json_data
    assert json_data['status'] == 'success'
    assert 'data' in json_data
    # Return detail data should be a dictionary, not a list
    assert isinstance(json_data['data'], dict)

def test_get_equipment_detail_not_found(client):
    """Test getting a single equipment detail for non-existent equipment."""
    response = client.get('/equipment/999')
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Equipment not found.'



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
