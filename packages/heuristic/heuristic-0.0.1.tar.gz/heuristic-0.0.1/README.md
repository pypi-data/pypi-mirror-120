******
|name|
******

.. image:: https://img.shields.io/pypi/v/sphinx_rtd_theme.svg
   :target: https://pypi.python.org/pypi/sphinx_rtd_theme
   :alt: Pypi Version
.. image:: https://readthedocs.org/projects/rep-nome2/badge/?version=latest
   :target: https://rep-nome2.readthedocs.io/pt/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://img.shields.io/pypi/l/sphinx_rtd_theme.svg
   :target: https://pypi.python.org/pypi/sphinx_rtd_theme/
   :alt: License
.. image:: https://readthedocs.org/projects/sphinx-rtd-theme/badge/?version=latest
  :target: http://sphinx-rtd-theme.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

A biblioteca_ xxxxxxxxxx. Documentação construida no `Read the Docs`_, é
possivel encontrar e ler alguns exemplos `aqui`_

.. _biblioteca: google.com
.. _Read the Docs: http://www.readthedocs.org
.. _aqui: google.com

Installation
============

Este pacote está disponível no PyPI_ e é pode ser instalado com o ``pip``:

.. code:: console

   $ pip install |name|

A baixo é um pequeno exemplo de como utilizar diferentes algoritmos para um
dado problema:

.. code:: python

	from pacote1_raiz import FireFly
	from pacote1_raiz import Pop, Abc, Pso, Sa


	nPop = 10
	nGen = 50
	ranges = np.array([[-50, 50]]*10)
	fun = rastrigin

	meta1 = Pso()
	meta2 = FireFly()
	meta3 = Abc()
	meta4 = Sa()
	  
	nRep = 100
	metas = {'Abc': [Pop(meta3, fun, ranges, int(nPop/2), nGen) for r in range(nRep)],
			 'Pso': [Pop(meta1, fun, ranges, nPop, nGen) for r in range(nRep)],
			 'FA': [Pop(meta2, fun, ranges, nPop, nGen) for r in range(nRep)],
			 'Sa': [Pop(meta4, fun, ranges, nPop, nGen) for r in range(nRep)]
			}

	for k, reps in tqdm(metas.items()):
		for r in reps:
			for g in range(1, nGen):
				next(r)

	for k, v in metas.items():
		bestRep = min(v, key=lambda m: m.pBest['value'][-1])
	   
		print('%s:' %k)
		print(bestRep.pBest['ch'][-1])
		print('FO:', bestRep.pBest['value'][-1])
		print()
		
Para mais informações consulte a pagina de instalação

.. _PyPI: https://pypi.python.org/pypi

Configuration
=============

This theme is highly customizable on both the page level and on a global level.
To see all the possible configuration options, read the documentation on
`configuring the theme`_.

.. _configuring the theme: google.com

Contributing
============

Se você gostaria de contribuir, siga as intruções no `guia de contribuição`_.

.. _guia de contribuição: https://sphinx-rtd-theme.readthedocs.io/en/latest/contributing.html

.. |name| replace:: Biblioteca do Joao
