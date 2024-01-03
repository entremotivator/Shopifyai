import streamlit as st
import requests
import json

# Feature 0: User Input for Shopify Store Information
st.title("Shopify Store Dashboard Configuration")
st.header("Enter Your Shopify Store Information")

shop_url = st.text_input("Shopify Store URL", "your-shop.myshopify.com")
api_key = st.text_input("Shopify API Key", "your-api-key")
api_password = st.text_input("Shopify API Password", "your-api-password", type="password")

# Shopify API base URL
api_base_url = f'https://{shop_url}/admin/api/2022-01'

# Function to authenticate with Shopify API
def authenticate():
    return (api_key, api_password)

# Feature 1: Display Store Information
st.title("Shopify Store Dashboard")
st.header("Store Information")

response = requests.get(f'{api_base_url}/shop.json', auth=authenticate())
shop_data = response.json().get('shop', {})

st.write(f"**Store Name:** {shop_data.get('name')}")
st.write(f"**Shop Owner:** {shop_data.get('shop_owner')}")
st.write(f"**Currency:** {shop_data.get('currency')}")

# Feature 2: List Products
st.header("Product Management")

response = requests.get(f'{api_base_url}/products.json', auth=authenticate())
products = response.json().get('products', [])

st.subheader("Product List")
for product in products:
    st.write(f"**{product['title']}** - {product['variants'][0]['price']} {shop_data['currency']}")
    if st.button(f"Update Price for {product['title']}"):
        new_price = st.number_input(f"New Price for {product['title']}", min_value=0.01, step=0.01, value=product['variants'][0]['price'])
        update_price_data = {
            "variant": {
                "id": product['variants'][0]['id'],
                "price": new_price
            }
        }
        response = requests.put(f'{api_base_url}/variants/{product["variants"][0]["id"]}.json', auth=authenticate(), json=update_price_data)
        if response.status_code == 200:
            st.success(f"Price updated successfully for {product['title']}.")
        else:
            st.error(f"Failed to update price. Status code: {response.status_code}, Error message: {response.text}")

# Feature 3: Create a New Page
st.header("Create a New Page")

new_page_title = st.text_input("Page Title")
new_page_content = st.text_area("Page Content", height=200)
create_page_button = st.button("Create Page")

if create_page_button:
    new_page_data = {
        "page": {
            "title": new_page_title,
            "body_html": new_page_content,
            "published": True
        }
    }
    response = requests.post(f'{api_base_url}/pages.json', auth=authenticate(), json=new_page_data)
    if response.status_code == 201:
        st.success("New page created successfully.")
    else:
        st.error(f"Failed to create new page. Status code: {response.status_code}, Error message: {response.text}")

# Feature 4: Order Analytics
st.header("Order Analytics")

response = requests.get(f'{api_base_url}/orders.json', auth=authenticate())
orders = response.json().get('orders', [])

st.subheader("Recent Orders")
for order in orders[:5]:
    st.write(f"Order #{order['order_number']} - Total: {order['total_price']} {shop_data['currency']}")

# Feature 5: Customer Management
st.header("Customer Management")

response = requests.get(f'{api_base_url}/customers.json', auth=authenticate())
customers = response.json().get('customers', [])

st.subheader("Recent Customers")
for customer in customers[:5]:
    st.write(f"{customer['first_name']} {customer['last_name']} - {customer['email']}")

# Feature 6: Search Orders by Order Number
st.header("Search Orders")

search_order_number = st.text_input("Enter Order Number to Search")
search_order_button = st.button("Search Order")

if search_order_button and search_order_number:
    response = requests.get(f'{api_base_url}/orders.json?name={search_order_number}', auth=authenticate())
    search_result = response.json().get('orders', [])
    if search_result:
        st.write(f"Order #{search_result[0]['order_number']} - Total: {search_result[0]['total_price']} {shop_data['currency']}")
    else:
        st.warning(f"No order found with order number {search_order_number}")

# Feature 7: Search Customers by Email
st.header("Search Customers")

search_customer_email = st.text_input("Enter Customer Email to Search")
search_customer_button = st.button("Search Customer")

if search_customer_button and search_customer_email:
    response = requests.get(f'{api_base_url}/customers.json?email={search_customer_email}', auth=authenticate())
    search_result = response.json().get('customers', [])
    if search_result:
        st.write(f"Customer: {search_result[0]['first_name']} {search_result[0]['last_name']} - Email: {search_result[0]['email']}")
    else:
        st.warning(f"No customer found with email {search_customer_email}")

# Feature 8: Additional Buttons
st.header("Additional Buttons")

button_actions = [
    {"label": "Button 1", "action": "Perform Action 1"},
    {"label": "Button 2", "action": "Perform Action 2"},
    # Add more buttons and actions as needed
]

for button_info in button_actions:
    if st.button(button_info["label"]):
        st.info(f"{button_info['action']}")

# Add more features based on your specific needs...
