FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN sed -i 's/http.kali.org/kali.download/g' /etc/apt/sources.list

RUN apt-get update \
&& apt-get install -qq -y systemd \
&& apt-get install -qq -y build-essential \
&& apt-get install -qq -y tzdata \
&& apt-get install -qq -y vim curl \
&& apt-get clean autoclean \
&& apt-get autoremove -y \
&& rm -rf /var/lib/{apt,dpkg,cache,log}

CMD ["/sbin/init"]
