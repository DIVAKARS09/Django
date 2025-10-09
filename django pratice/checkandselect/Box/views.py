from django.shortcuts import render

# NOTE: Using global variables like this is for demonstration only. 
# In a real Django app, use a database or session for persistent data.
all_items = []
saved_items = []
item_being_edited = None 
message = None 

def index(request):

    global all_items, saved_items, item_being_edited, message 
    
    temp_message = message
    message = None
    
    if request.method == 'POST':
        if 'add_item' in request.POST:
            new_item_name = request.POST.get('item_name', '').strip()
            new_item_quantity = request.POST.get('item_quantity')
            
            # --- START ITEM & QUANTITY SEPARATE VALIDATION ---
            error_parts = []
            if not new_item_name:
                error_parts.append("Item Name is required.")
            if not new_item_quantity:
                error_parts.append("Quantity is required.")
                
            if error_parts:
                 # Combine messages for a single pop-up
                 message = "ERROR: " + " ".join(error_parts) 
            # --- END ITEM & QUANTITY SEPARATE VALIDATION ---
            
            else:
                new_item = {'name': new_item_name, 'quantity': new_item_quantity}
                name_exists = any(item['name'] == new_item_name for item in all_items)

                if name_exists:
                    message = f"ERROR: Item '{new_item_name}' already exists."
                else:
                    all_items.append(new_item)
                    message = f"SUCCESS: Item '{new_item_name}' added."

        elif 'save_selected' in request.POST:
            selected_names = request.POST.getlist('selected_items')
            
            saved_items = selected_names
            message = f"SUCCESS: {len(saved_items)} item(s) saved."
            item_being_edited = None 

        elif 'edit_start' in request.POST:
            item_to_edit_name = request.POST.get('edit_start')
            item_being_edited = item_to_edit_name

        elif 'edit_finish' in request.POST:
            old_name = request.POST.get('edit_finish')
            new_name = request.POST.get('new_item_name', '').strip()
            new_quantity = request.POST.get('new_item_quantity')

            item_dict = next((item for item in all_items if item['name'] == old_name), None)
            
            if not new_name or not new_quantity:
                 message = f"ERROR: Edit failed for '{old_name}'. Name and quantity cannot be empty."
            
            elif item_dict:
                old_quantity = item_dict.get('quantity')
                
                name_changed = (new_name != old_name)
                quantity_changed = (str(new_quantity) != str(old_quantity))

                if name_changed and not quantity_changed:
                    message = f"SUCCESS: Item name updated from '{old_name}' to '{new_name}'."
                elif quantity_changed and not name_changed:
                    message = f"SUCCESS: Quantity updated for item '{old_name}'."
                elif name_changed and quantity_changed:
                    message = f"SUCCESS: Item name and quantity updated for '{old_name}'."
                else:
                    message = f"SUCCESS: No changes detected for item '{old_name}'."
                
                if 'SUCCESS:' in message:
                    item_dict['name'] = new_name
                    item_dict['quantity'] = new_quantity
                    
                    if old_name in saved_items and name_changed:
                        try:
                            saved_index = saved_items.index(old_name)
                            saved_items[saved_index] = new_name
                        except ValueError:
                            pass
            
            if message and 'ERROR:' in message:
                item_being_edited = old_name 
            else:
                item_being_edited = None
            
        elif 'remove_item' in request.POST:
            item_to_remove_name = request.POST.get('remove_item')
            
            original_length = len(all_items)
            
            all_items = [item for item in all_items if item['name'] != item_to_remove_name]
            
            if len(all_items) < original_length:
                 message = f"SUCCESS: Item '{item_to_remove_name}' removed."
            else:
                 message = f"ERROR: Item '{item_to_remove_name}' not found for removal."
            
            if item_to_remove_name in saved_items:
                saved_items.remove(item_to_remove_name)
                
            if item_to_remove_name == item_being_edited:
                item_being_edited = None

    if message is None:
        message = temp_message
        
    return render(request, 'index.html', {
        'items': all_items,
        'saved_items': saved_items,
        'item_being_edited': item_being_edited, 
        'message': message,
    })