ARG ODOO_VERSION
FROM odoo:${ODOO_VERSION}

USER root

#RUN pip3 install --no-cache-dir \
#    pandas \
#    redis \
#    seaborn \
#    matplotlib \
#    debugpy \
#    --break-system-packages \

RUN mkdir -p /mnt/extra-addons \
    && chown -R odoo:odoo /mnt/extra-addons /var/lib/odoo

USER odoo

ENV ODOO_RC /etc/odoo/odoo.conf