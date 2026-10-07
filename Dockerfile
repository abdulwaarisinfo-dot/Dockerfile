FROM mysql:8.0

# --datadir ek subfolder mein rakha hai taaki Render disk ka `lost+found`
# folder MySQL ke initialize hone mein dikkat na kare.
CMD ["--datadir=/var/lib/mysql/data", "--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]
