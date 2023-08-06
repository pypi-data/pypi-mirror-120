
nayose is a Python module for data cleansing for Japanese address and is distributed under the MIT license.

Installation
============

You can install the latest this module with the command:

    pip install nayose

Quick start
============

nayose has two main function of data cleansing for Japanese address.

`complement_address` is a function to complement dirty address. For example, the followings is a case of missing state(都道府県).

    from nayose import complement_address

    complement_address("千代田区大手町1−1−1大手町あいうえビル")
    > "東京都千代田区大手町1−1−1大手町あいうえビル"


`split_address` is a function to split full address to state(都道府県), city(市区郡) and street(その他).

    from nayose import split_address

    split_address("東京都千代田区大手町1−1−1大手町あいうえビル")
    > ('東京都', '千代田区', '大手町1−1−1大手町あいうえビル')


Important links
============

- Official source code repo: https://github.com/sonesuke/nayose
- Download releases: https://pypi.org/project/nayose/
- Issue tracker: https://github.com/sonesuke/nayose/issues

Citation
============

If you use nayose in a publication, we would appreciate citations: https://github.com/sonesuke/nayose


For contributors
============

You can contribute it quickly by using docker image with the command.

    git clone https://github.com/sonesuke/nayose.git
    docker-compose run nayose bash


For test.

    bash scripts/test


If you add any modules, please re-build docker image after 'poetry update' .



