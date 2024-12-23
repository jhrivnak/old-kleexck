import pygame
from .world import screen_width, screen_height, font

try:
    from .levels.home.home import HomeLevel
except ImportError:
    from src.levels.home.home import HomeLevel

class Inventory:
    def __init__(self):
        self.visible = False
        self.items = {}  # Dictionary to store items and their quantities
        self.money = 3.50  # Starting money
        self.slots = 16  # Number of inventory slots
        
        # Inventory UI dimensions
        self.width = 300
        self.height = 400
        self.slot_size = 50
        self.padding = 10
        
        # Position inventory window in center of screen
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # Create inventory surface
        self.surface = pygame.Surface((self.width, self.height))
        
        self.last_toggle_time = 0
        self.toggle_cooldown = 200  # milliseconds
        
        # Fixed tooltip area
        self.tooltip_height = 80
        self.tooltip_padding = 15
        
        # Dragging state
        self.dragged_item = None
        self.dragged_from_index = None
        
        # Mouse hover text
        self.hover_font = pygame.font.SysFont(None, 20)
        
        # Load sounds
        self.pickup_sound = pygame.mixer.Sound("assets/audio/effects/inventory/pickUpGlass.ogg")
        self.putdown_sound = pygame.mixer.Sound("assets/audio/effects/inventory/putDownGlass.ogg")
        
        self.current_level = None  # Will be set by the game
        self.confirm_delete = False
        self.item_to_delete = None
        self.confirm_text = None

    def add_item(self, item_name, item_image):
        if len(self.items) < self.slots:
            # Find first available slot
            slot = 0
            while any(data.get('slot') == slot for data in self.items.values()):
                slot += 1
                if slot >= self.slots:
                    return False
                
            scaled_image = pygame.transform.scale(item_image, (40, 40))
            self.items[item_name] = {
                'image': scaled_image,
                'quantity': 1,
                'slot': slot
            }
            return True
        return False
        
    def toggle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_toggle_time > self.toggle_cooldown:
            self.visible = not self.visible
            self.last_toggle_time = current_time
            
    def handle_click(self, mouse_pos, is_clicking):
        if not self.visible:
            return
            
        adjusted_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        in_inventory = (0 <= adjusted_pos[0] <= self.width and 
                       0 <= adjusted_pos[1] <= self.height)
        
        # Handle confirmation dialog if it's showing
        if self.confirm_delete:
            if is_clicking:
                # Check for Yes/No click
                yes_rect = pygame.Rect(self.width//2 - 60, self.height//2 + 20, 50, 20)
                no_rect = pygame.Rect(self.width//2 + 10, self.height//2 + 20, 50, 20)
                
                if yes_rect.collidepoint(adjusted_pos):
                    # Confirmed delete
                    self.putdown_sound.play()
                    if isinstance(self.current_level, HomeLevel):
                        self.current_level.crack_visible = True
                    self.confirm_delete = False
                    self.item_to_delete = None
                elif no_rect.collidepoint(adjusted_pos):
                    # Cancelled delete - put item back in inventory
                    if self.item_to_delete:
                        self.return_item_to_inventory(self.item_to_delete)
                    self.confirm_delete = False
                    self.item_to_delete = None
                return

        # Normal inventory handling
        if is_clicking:  # Mouse button pressed
            if in_inventory:
                slot_clicked = self.get_slot_at_position(adjusted_pos)
                if slot_clicked is not None:
                    # Find if there's an item in this slot
                    for item_name, item_data in self.items.items():
                        if item_data.get('slot') == slot_clicked and not self.dragged_item:
                            self.dragged_item = (item_name, item_data)
                            self.pickup_sound.play()
                            del self.items[item_name]
                            break
        else:  # Mouse button released
            if self.dragged_item:
                if in_inventory:
                    slot = self.get_slot_at_position(adjusted_pos)
                    if slot is not None:
                        # Place item in this slot
                        item_name, item_data = self.dragged_item
                        item_data['slot'] = slot
                        self.items[item_name] = item_data
                        self.putdown_sound.play()
                    else:
                        # No valid slot, return item to inventory
                        self.return_item_to_inventory(self.dragged_item)
                else:
                    # Drop item at player's feet
                    if isinstance(self.current_level, HomeLevel) and self.dragged_item[0] == "crackpipe":
                        self.current_level.crack_visible = True
                        # Position crack at player's feet
                        self.current_level.crack_rect.x = self.current_level.player.x
                        self.current_level.crack_rect.y = self.current_level.player.y + 32  # Just below player
                        self.putdown_sound.play()
                    else:
                        # If not in home level or not crack, return to inventory
                        self.return_item_to_inventory(self.dragged_item)
                self.dragged_item = None

    def get_slot_at_position(self, pos):
        """Convert mouse position to inventory slot number"""
        x, y = pos
        
        # Check if we're in the slots area
        slots_start_x = self.padding
        slots_start_y = self.padding
        slot_total_size = self.slot_size + self.padding
        
        # Calculate relative position in grid
        rel_x = x - slots_start_x
        rel_y = y - slots_start_y
        
        # Calculate row and column
        col = rel_x // slot_total_size
        row = rel_y // slot_total_size
        
        # Validate position
        if (0 <= col < 4 and 0 <= row < 4 and
            rel_x % slot_total_size < self.slot_size and
            rel_y % slot_total_size < self.slot_size):
            return row * 4 + col
        return None

    def return_item_to_inventory(self, item):
        """Put an item back in the first available slot"""
        if item:
            item_name, item_data = item
            # Find first available slot
            for i in range(self.slots):
                if not any(data.get('slot') == i for data in self.items.values()):
                    item_data['slot'] = i
                    self.items[item_name] = item_data
                    break

    def draw(self, screen):
        if not self.visible:
            return
            
        # Draw inventory background
        self.surface.fill((70, 70, 70))
        pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.width, self.height), 2)
        
        # Draw fixed tooltip area at bottom
        tooltip_area = pygame.Rect(
            self.padding,
            self.height - self.tooltip_height - self.padding - 30,
            self.width - (self.padding * 2),
            self.tooltip_height
        )
        pygame.draw.rect(self.surface, (50, 50, 50), tooltip_area)
        pygame.draw.rect(self.surface, (100, 100, 100), tooltip_area, 1)
        
        # Draw slots and track hovered item
        hovered_item = None
        mouse_pos = pygame.mouse.get_pos()
        adjusted_mouse_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
        
        # Draw slots
        for i in range(self.slots):
            row = i // 4
            col = i % 4
            x = self.padding + (col * (self.slot_size + self.padding))
            y = self.padding + (row * (self.slot_size + self.padding))
            
            pygame.draw.rect(self.surface, (50, 50, 50), 
                           (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(self.surface, (100, 100, 100), 
                           (x, y, self.slot_size, self.slot_size), 1)
        
        # Draw items that aren't being dragged
        for item_name, item_data in self.items.items():
            slot = item_data.get('slot', 0)
            row = slot // 4
            col = slot % 4
            x = self.padding + (col * (self.slot_size + self.padding)) + 5
            y = self.padding + (row * (self.slot_size + self.padding)) + 5
            
            self.surface.blit(item_data['image'], (x, y))
            
            # Check for hover
            item_rect = pygame.Rect(x, y, 40, 40)
            if item_rect.collidepoint(adjusted_mouse_pos):
                hovered_item = item_name
        
        # Draw tooltip in fixed area if item is hovered
        if hovered_item:
            self.draw_fixed_tooltip(hovered_item, tooltip_area)
        
        # Draw money at bottom
        money_text = font.render(f"${self.money:.2f}", True, (255, 215, 0))
        money_rect = money_text.get_rect(bottomright=(self.width - 10, self.height - 10))
        self.surface.blit(money_text, money_rect)
        
        # Draw the inventory surface first
        screen.blit(self.surface, (self.x, self.y))
        
        # Draw hover text and dragged item AFTER inventory surface
        if hovered_item:
            self.draw_hover_text(screen, mouse_pos, hovered_item)
        
        # Draw dragged item at mouse position if any
        if self.dragged_item:
            item_name, item_data = self.dragged_item
            drag_x = mouse_pos[0] - 20  # Center item on mouse
            drag_y = mouse_pos[1] - 20
            screen.blit(item_data['image'], (drag_x, drag_y))
            self.draw_hover_text(screen, mouse_pos, item_name)
        
        # Draw confirmation dialog if needed
        if self.confirm_delete:
            # Draw dialog box
            dialog_rect = pygame.Rect(
                self.width//4,
                self.height//3,
                self.width//2,
                self.height//3
            )
            pygame.draw.rect(self.surface, (40, 40, 40), dialog_rect)
            pygame.draw.rect(self.surface, (100, 100, 100), dialog_rect, 2)
            
            # Draw text
            text = font.render(self.confirm_text, True, (255, 255, 255))
            text_rect = text.get_rect(centerx=self.width//2, centery=self.height//2)
            self.surface.blit(text, text_rect)
            
            # Draw buttons
            yes_text = font.render("Yes", True, (255, 255, 255))
            no_text = font.render("No", True, (255, 255, 255))
            
            yes_rect = pygame.Rect(self.width//2 - 60, self.height//2 + 20, 50, 20)
            no_rect = pygame.Rect(self.width//2 + 10, self.height//2 + 20, 50, 20)
            
            pygame.draw.rect(self.surface, (60, 60, 60), yes_rect)
            pygame.draw.rect(self.surface, (60, 60, 60), no_rect)
            pygame.draw.rect(self.surface, (100, 100, 100), yes_rect, 1)
            pygame.draw.rect(self.surface, (100, 100, 100), no_rect, 1)
            
            self.surface.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
            self.surface.blit(no_text, no_text.get_rect(center=no_rect.center))
        
    def draw_fixed_tooltip(self, item_name, area):
        if item_name == "crackpipe":
            title = "[Low Quality Crack]"
            lines = [
                "Increases movement speed for 30 seconds",
                "Causes cancer"
            ]
            
            # Draw title with outline effect
            title_font = pygame.font.SysFont(None, 24)
            title_text = title_font.render(title, True, (0, 0, 0))
            title_outline = title_font.render(title, True, (255, 255, 150))
            
            # Center title in tooltip area
            title_x = area.x + (area.width // 2) - (title_text.get_width() // 2)
            title_y = area.y + self.tooltip_padding
            
            # Draw title outline and text
            for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                self.surface.blit(title_outline, (title_x + dx, title_y + dy))
            self.surface.blit(title_text, (title_x, title_y))
            
            # Draw description lines
            desc_font = pygame.font.SysFont(None, 20)
            for i, line in enumerate(lines):
                text = desc_font.render(line, True, (200, 200, 200))
                x = area.x + self.tooltip_padding
                y = title_y + title_text.get_height() + (i * 20) + 10
                self.surface.blit(text, (x, y))
        
    def draw_hover_text(self, screen, mouse_pos, item_name):
        if item_name == "crackpipe":
            text = self.hover_font.render("Low Quality Crack", True, (0, 0, 0))
            outline = self.hover_font.render("Low Quality Crack", True, (255, 255, 150))
            
            # Position text near mouse cursor but ensure it stays on screen
            text_width = text.get_width()
            text_height = text.get_height()
            text_x = min(mouse_pos[0] + 15, screen_width - text_width - 10)
            text_y = min(max(mouse_pos[1] - 15, text_height), screen_height - text_height - 10)
            
            # Draw outline by offsetting text slightly in each direction
            for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                screen.blit(outline, (text_x + dx, text_y + dy))
            screen.blit(text, (text_x, text_y))
        
    def set_current_level(self, level):
        self.current_level = level
        