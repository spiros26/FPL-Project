import pandas as pd
from tqdm import tqdm
from modules.useful_functions import convert

def players_data(id_dict_df, ids, PATH):
    # Add some more data by hand (I hate Brazilian/Potugese Names)
    # 2021-22
    understat_dfs_2021 = [
                    pd.read_csv(PATH + '2021-22/understat/Joelinton_87.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Thiago_Alcántara_229.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Kevin_De_Bruyne_447.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Philippe_Coutinho_488.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Mohamed_Elneny_496.csv'),
                    pd.read_csv(PATH + '2021-22/understat/David_de_Gea_546.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fernandinho_614.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Virgil_van_Dijk_833.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Oriol_Romeu_842.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Samir_1142.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Bruno_Fernandes_1228.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Emerson_7430.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Alisson_1257.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Allan_1379.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Jorginho_1389.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Johann_Berg_Gudmundsson_1663.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Alex_Telles_1828.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Emiliano_Buendía_2203.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Jonny_2280.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Cristiano_Ronaldo_2371.csv'),
                    pd.read_csv(PATH + '2021-22/understat/João_Cancelo_2379.csv'),
                    pd.read_csv(PATH + '2021-22/understat/André_Gomes_2383.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Thiago_Silva_3288.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Lucas_Moura_3293.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ricardo_Pereira_3303.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fabinho_3420.csv'),
                    pd.read_csv(PATH + '2021-22/understat/João_Moutinho_3422.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Bernardo_Silva_3635.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Kiko_Femenía_5043.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Gabriel_Jesus_5543.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Anwar_El_Ghazi_5612.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Giovani_Lo_Celso_5681.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Richarlison_6026.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ederson_6054.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Douglas_Luiz_6122.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Nélson_Semedo_6163.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Pedro_Neto_6382.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Júnior_Firpo_6485.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Oghenekaro_Etebo_6538.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rayan_Ait_Nouri_6674.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fred_6817.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rúben_Neves_6853.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Juan_Camilo_Hernández_6954.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Emile_Smith-Rowe_7230.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Diogo_Dalot_7281.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ezri_Konsa_Ngoyo_7726.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Gabriel_Martinelli_7752.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Raphinha_8026.csv'),
                    pd.read_csv(PATH + '2021-22/understat/João_Pedro_8272.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Daniel_Podence_8291.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Bruno_Guimarães_8327.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Alexis_Mac_Allister_8379.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Trincão_8934.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rúben_Dias_8961.csv'),
                    pd.read_csv(PATH + '2021-22/understat/David_Raya_9676.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Mads_Bech_Sørensen_9683.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Mads_Roerslev_9685.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Albert_Sambi_Lokonga_9689.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Nuno_Tavares_9691.csv'),
                    pd.read_csv(PATH + '2021-22/understat/José_Sá_9740.csv')

    ]

    main_dfs_2021 = [
                pd.read_csv(PATH + '2021-22/players/Joelinton Cássio_Apolinário de Lira_310/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Thiago_Alcántara do Nascimento_225/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Kevin_De Bruyne_251/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Philippe_Coutinho Correia_681/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Mohamed Naser_El Sayed Elneny_12/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/David_de Gea_270/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Fernando_Luiz Rosa_453/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Virgil_van Dijk_229/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Oriol_Romeu Vidal_335/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Samir_Caetano de Souza Santos_677/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Bruno Miguel_Borges Fernandes_277/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Emerson Aparecido_Leite de Souza Junior_588/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Alisson_Ramses Becker_231/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Allan_Marques Loureiro_171/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Jorge Luiz_Frello Filho_123/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Johann Berg_Gudmundsson_108/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Alex Nicolao_Telles_279/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Emiliano_Buendía Stati_43/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Jonathan_Castro Otto_433/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Cristiano Ronaldo_dos Santos Aveiro_579/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/João Pedro Cavaco_Cancelo_256/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/André Filipe_Tavares Gomes_172/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Thiago_Emiliano da Silva_121/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Lucas_Rodrigues Moura da Silva_362/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Ricardo Domingos_Barbosa Pereira_207/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Fabio Henrique_Tavares_232/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/João Filipe Iria_Santos Moutinho_426/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Bernardo Mota_Veiga de Carvalho e Silva_261/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Francisco_Femenía Far_382/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Gabriel Fernando_de Jesus_263/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Anwar_El Ghazi_42/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Giovani_Lo Celso_372/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Richarlison_de Andrade_180/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Ederson_Santana de Moraes_257/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Douglas Luiz_Soares de Paulo_50/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Nélson_Cabral Semedo_437/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Pedro_Lomba Neto_441/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Héctor Junior_Firpo Adames_463/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Oghenekaro Peter_Etebo_467/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Rayan_Ait Nouri_470/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Frederico_Rodrigues de Paula Santos_274/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Rúben Diogo_da Silva Neves_436/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Juan Camilo_Hernández Suárez_472/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Emile_Smith Rowe_21/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/José Diogo_Dalot Teixeira_510/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Ezri_Konsa Ngoyo_45/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Gabriel Teodoro_Martinelli Silva_26/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Raphael_Dias Belloli_196/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/João Pedro_Junqueira de Jesus_404/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Daniel_Castelo Podence_438/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Bruno_Guimarães Rodriguez Moura_697/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Alexis_Mac Allister_74/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Francisco_Machado Mota de Castro Trincão_461/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Rúben Santos_Gato Alves Dias_262/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/David_Raya Martin_80/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Mads_Bech Sørensen_90/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Mads_Roerslev Rasmussen_89/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Albert_Sambi Lokonga_478/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/Nuno_Varela Tavares_466/gw.csv'),
                pd.read_csv(PATH + '2021-22/players/José_Malheiro de Sá_475/gw.csv')
    ]


    understat_dfs_promoted_players_2020 = [
                 pd.read_csv(PATH + '2021-22/understat/Maxime_Le_Marchand_3304.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Tom_Cairney_6835.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Tim_Ream_7184.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Michael_Hector_5274.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Neeskens_Kebano_6840.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Bobby_Reid_6827.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Joe_Bryan_6834.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Aleksandar_Mitrovic_773.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Marek_Rodák_8704.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Ivan_Cavaleiro_3683.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Josh_Onomah_661.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Aboubakar_Kamara_4866.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Franck_Zambo_6434.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Harrison_Reed_910.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Antonee_Robinson_8940.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Mario_Lemina_1299.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Kenny_Tete_5973.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Denis_Odoi_7077.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Ola_Aina_725.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Tosin_Adarabioyo_5590.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Josh_Maja_5587.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Rhian_Brewster_5569.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Billy_Sharp_7712.csv'),
                 pd.read_csv(PATH + '2021-22/understat/David_McGoldrick_7711.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Chris_Basham_7704.csv'),
                 pd.read_csv(PATH + '2021-22/understat/John_Fleck_7709.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Enda_Stevens_7707.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Oliver_Norwood_7710.csv'),
                 pd.read_csv(PATH + '2021-22/understat/George_Baldock_7706.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Jack_Robinson_8286.csv'),
                 pd.read_csv(PATH + '2021-22/understat/John_Egan_7703.csv'),
                 pd.read_csv(PATH + '2021-22/understat/John_Lundstram_7708.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Ben_Osborn_7714.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Oliver_McBurnie_1736.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Sander_Berge_8285.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Oliver_Burke_5256.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Ethan_Ampadu_6369.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Phil_Jagielka_587.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Callum_Robinson_4476.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Kieran_Gibbs_545.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Hal_Robson-Kanu_1738.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Jake_Livermore_1689.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Kamil_Grosicki_3231.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Matt_Phillips_1737.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Kyle_Bartley_964.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Romaine_Sawyers_8757.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Sam_Johnstone_978.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Conor_Townsend_8905.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Semi_Ajayi_4490.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Kyle_Edwards_8758.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Darnell_Furlong_4391.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Sam_Field_1013.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Rekeem_Harper_5562.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Robert_Snodgrass_1691.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Grady_Diangana_6651.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Matheus_Pereira_7153.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Branislav_Ivanovic_682.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Karlan_Grant_7390.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Mbaye_Diagne_9290.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Willian_700.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Dani_Ceballos_2446.csv'),
                 pd.read_csv(PATH + '2021-22/understat/James_Rodríguez_2249.csv')
    ]

    main_dfs_promoted_players_2020 = [
                pd.read_csv(PATH + '2020-21/players/Maxime_Le Marchand_173/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Tom_Cairney_175/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Tim_Ream_176/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Michael_Hector_178/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Neeskens_Kebano_180/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Bobby_Decordova-Reid_181/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Joe_Bryan_182/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Aleksandar_Mitrović_184/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Marek_Rodák_186/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Ivan Ricardo_Neves Abreu Cavaleiro_187/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Josh_Onomah_188/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Aboubakar_Kamara_190/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/André-Frank_Zambo Anguissa_191/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Harrison_Reed_373/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Antonee_Robinson_484/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Mario_Lemina_493/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Kenny_Tete_517/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Denis_Odoi_525/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Ola_Aina_562/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Tosin_Adarabioyo_572/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Josh_Maja_665/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Rhian_Brewster_262/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Billy_Sharp_343/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/David_McGoldrick_344/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Chris_Basham_345/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/John_Fleck_346/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Enda_Stevens_347/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Oliver_Norwood_349/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/George_Baldock_351/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Jack_Robinson_352/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/John_Egan_353/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/John_Lundstram_355/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Ben_Osborn_356/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Oliver_McBurnie_357/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Sander_Berge_360/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Oliver_Burke_424/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Ethan_Ampadu_509/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Phil_Jagielka_529/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Callum_Robinson_358/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Kieran_Gibbs_407/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Hal_Robson-Kanu_408/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Jake_Livermore_409/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Kamil_Grosicki_410/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Matt_Phillips_411/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Kyle_Bartley_412/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Romaine_Sawyers_413/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Sam_Johnstone_417/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Conor_Townsend_418/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Oluwasemilogo Adesewo Ibidapo_Ajayi_419/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Kyle_Edwards_421/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Darnell_Furlong_422/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Sam_Field_423/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Rekeem_Harper_426/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Robert_Snodgrass_428/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Grady_Diangana_446/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Matheus_Pereira_481/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Branislav_Ivanovic_530/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Karlan_Grant_582/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Mbaye_Diagne_648/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Willian_Borges Da Silva_478/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Daniel_Ceballos Fernández_501/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/James_Rodríguez_508/gw.csv')
    ]

    # Add some more data by hand (I hate Brazilian/Potugese Names)
        # 2020-21
    understat_dfs_2020 = [
                    pd.read_csv(PATH + '2021-22/understat/Joelinton_87.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Thiago_Alcántara_229.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Kevin_De_Bruyne_447.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Mohamed_Elneny_496.csv'),
                    pd.read_csv(PATH + '2021-22/understat/David_de_Gea_546.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fernandinho_614.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Virgil_van_Dijk_833.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Oriol_Romeu_842.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Bruno_Fernandes_1228.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Alisson_1257.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Allan_1379.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Jorginho_1389.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Alex_Telles_1828.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Jonny_2280.csv'),
                    pd.read_csv(PATH + '2021-22/understat/João_Cancelo_2379.csv'),
                    pd.read_csv(PATH + '2021-22/understat/André_Gomes_2383.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Lucas_Moura_3293.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ricardo_Pereira_3303.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fabinho_3420.csv'),
                    pd.read_csv(PATH + '2021-22/understat/João_Moutinho_3422.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Bernardo_Silva_3635.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Gabriel_Jesus_5543.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Anwar_El_Ghazi_5612.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Giovani_Lo_Celso_5681.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Richarlison_6026.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ederson_6054.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Douglas_Luiz_6122.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Nélson_Semedo_6163.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Pedro_Neto_6382.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rayan_Ait_Nouri_6674.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fred_6817.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rui_Patrício_6849.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rúben_Neves_6853.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Emile_Smith-Rowe_7230.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Diogo_Dalot_7281.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ezri_Konsa_Ngoyo_7726.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Gabriel_Martinelli_7752.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Raphinha_8026.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Daniel_Podence_8291.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Alexis_Mac_Allister_8379.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rúben_Dias_8961.csv')
    ]

    main_dfs_2020 = [
                pd.read_csv(PATH + '2020-21/players/Joelinton Cássio_Apolinário de Lira_340/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Thiago_Alcántara do Nascimento_531/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Kevin_De Bruyne_272/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Mohamed Naser_El Sayed Elneny_526/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/David_de Gea_291/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Fernando_Luiz Rosa_266/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Virgil_van Dijk_250/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Oriol_Romeu Vidal_364/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Bruno Miguel_Borges Fernandes_302/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Alisson_Ramses Becker_252/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Allan_Marques Loureiro_502/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Jorge Luiz_Frello Filho_105/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Alex Nicolao_Telles_568/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Jonathan_Castro Otto_462/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/João Pedro Cavaco_Cancelo_277/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/André Filipe_Tavares Gomes_158/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Lucas_Rodrigues Moura da Silva_392/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Ricardo Domingos_Barbosa Pereira_226/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Fabio Henrique_Tavares_253/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/João Filipe Iria_Santos Moutinho_454/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Bernardo Mota_Veiga de Carvalho e Silva_281/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Gabriel Fernando_de Jesus_282/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Anwar_El Ghazi_45/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Giovani_Lo Celso_403/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Richarlison_de Andrade_166/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Ederson_Santana de Moraes_278/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Douglas Luiz_Soares de Paulo_52/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Nélson_Cabral Semedo_546/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Pedro_Lomba Neto_474/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Rayan_Ait Nouri_563/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Frederico_Rodrigues de Paula Santos_299/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Rui Pedro_dos Santos Patrício_455/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Rúben Diogo_da Silva Neves_466/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Emile_Smith Rowe_23/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/José Diogo_Dalot Teixeira_314/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Ezri_Konsa Ngoyo_46/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Gabriel Teodoro_Martinelli Silva_26/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Raphael_Dias Belloli_570/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Daniel_Castelo Podence_469/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Alexis_Mac Allister_80/gw.csv'),
                pd.read_csv(PATH + '2020-21/players/Rúben Santos_Gato Alves Dias_556/gw.csv')
    ]


    understat_dfs_promoted_players_2019 = [
                 pd.read_csv(PATH + '2021-22/understat/Billy_Sharp_7712.csv'),
                 pd.read_csv(PATH + '2021-22/understat/David_McGoldrick_7711.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Chris_Basham_7704.csv'),
                 pd.read_csv(PATH + '2021-22/understat/John_Fleck_7709.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Enda_Stevens_7707.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Oliver_Norwood_7710.csv'),
                 pd.read_csv(PATH + '2021-22/understat/George_Baldock_7706.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Jack_Robinson_8286.csv'),
                 pd.read_csv(PATH + '2021-22/understat/John_Egan_7703.csv'),
                 pd.read_csv(PATH + '2021-22/understat/John_Lundstram_7708.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Ben_Osborn_7714.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Oliver_McBurnie_1736.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Sander_Berge_8285.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Phil_Jagielka_587.csv'),
                 pd.read_csv(PATH + '2021-22/understat/Dan_Gosling_462.csv')
    ]

    main_dfs_promoted_players_2019 = [
                pd.read_csv(PATH + '2019-20/players/Billy_Sharp_298/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/David_McGoldrick_303/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Chris_Basham_423/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/John_Fleck_301/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Enda_Stevens_291/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Oliver_Norwood_302/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/George_Baldock_294/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Jack_Robinson_611/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/John_Egan_295/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/John_Lundstram_297/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Ben_Osborn_472/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Oliver_McBurnie_501/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Sander_Berge_621/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Phil_Jagielka_444/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Dan_Gosling_81/gw.csv')           
    ]

    # Add some more data by hand (I hate Brazilian/Potugese Names)
    # 2019-20
    understat_dfs_2019 = [
                    pd.read_csv(PATH + '2021-22/understat/Joelinton_87.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Kevin_De_Bruyne_447.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Mohamed_Elneny_496.csv'),
                    pd.read_csv(PATH + '2021-22/understat/David_de_Gea_546.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fernandinho_614.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Virgil_van_Dijk_833.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Oriol_Romeu_842.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Bruno_Fernandes_1228.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Alisson_1257.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Jorginho_1389.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Jonny_2280.csv'),
                    pd.read_csv(PATH + '2021-22/understat/João_Cancelo_2379.csv'),
                    pd.read_csv(PATH + '2021-22/understat/André_Gomes_2383.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Lucas_Moura_3293.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ricardo_Pereira_3303.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fabinho_3420.csv'),
                    pd.read_csv(PATH + '2021-22/understat/João_Moutinho_3422.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Bernardo_Silva_3635.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Gabriel_Jesus_5543.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Anwar_El_Ghazi_5612.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Giovani_Lo_Celso_5681.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Richarlison_6026.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ederson_6054.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Douglas_Luiz_6122.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Pedro_Neto_6382.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Fred_6817.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rui_Patrício_6849.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Rúben_Neves_6853.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Emile_Smith-Rowe_7230.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Diogo_Dalot_7281.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Ezri_Konsa_Ngoyo_7726.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Gabriel_Martinelli_7752.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Daniel_Podence_8291.csv'),
                    pd.read_csv(PATH + '2021-22/understat/Alexis_Mac_Allister_8379.csv')
    ]

    main_dfs_2019 = [
                pd.read_csv(PATH + '2019-20/players/Joelinton Cássio_Apolinário de Lira_466/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Kevin_De Bruyne_215/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Mohamed_Elneny_20/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/David_de Gea_235/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Fernando_Luiz Rosa_221/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Virgil_van Dijk_183/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Oriol_Romeu Vidal_328/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Bruno Miguel_Borges Fernandes_618/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Alisson_Ramses Becker_189/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Jorge Luiz_Frello Filho_118/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Jonathan_Castro Otto_402/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/João Pedro Cavaco_Cancelo_518/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/André Filipe_Tavares Gomes_422/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Lucas_Rodrigues Moura da Silva_345/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Ricardo Domingos_Barbosa Pereira_159/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Fabio Henrique_Tavares_197/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/João Filipe Iria_Santos Moutinho_415/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Bernardo Mota_Veiga de Carvalho e Silva_218/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Gabriel Fernando_de Jesus_211/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Anwar_El Ghazi_30/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Giovani_Lo Celso_523/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Richarlison_de Andrade_150/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Ederson_Santana de Moraes_212/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Douglas Luiz_Soares de Paulo_470/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Pedro_Lomba Neto_528/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Frederico_Rodrigues de Paula Santos_244/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Rui Pedro_dos Santos Patrício_411/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Rúben Diogo_da Silva Neves_414/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Emile_Smith Rowe_576/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/José Diogo_Dalot Teixeira_229/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Ezri_Konsa Ngoyo_452/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Gabriel Teodoro_Martinelli Silva_504/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Daniel_Castelo Podence_619/gw.csv'),
                pd.read_csv(PATH + '2019-20/players/Alexis_Mac Allister_627/gw.csv')
    ]

    # Add some more data by hand (I hate Brazilian/Potugese Names)
      # 2022-23


    season = '2022-23'
    understat_dfs_2022 = [
                    pd.read_csv(PATH +  season + '/understat/Joelinton_87.csv'),
                    pd.read_csv(PATH +  season + '/understat/Thiago_Alcántara_229.csv'),
                    pd.read_csv(PATH + season + '/understat/Kevin_De_Bruyne_447.csv'),
                    pd.read_csv(PATH + season + '/understat/Philippe_Coutinho_488.csv'),
                #    pd.read_csv(PATH + season + '/understat/Mohamed_Elneny_496.csv'),
                    pd.read_csv(PATH + season + '/understat/David_de_Gea_546.csv'),
                    pd.read_csv(PATH + season + '/understat/Virgil_van_Dijk_833.csv'),
                    pd.read_csv(PATH + season + '/understat/Oriol_Romeu_842.csv'),
                    pd.read_csv(PATH + season + '/understat/Bruno_Fernandes_1228.csv'),
                    pd.read_csv(PATH + season + '/understat/Emerson_7430.csv'),
                    pd.read_csv(PATH + season + '/understat/Alisson_1257.csv'),
                #     pd.read_csv(PATH + season + '/understat/Allan_1379.csv'),
                    pd.read_csv(PATH + season + '/understat/Jorginho_1389.csv'),
                #     pd.read_csv(PATH + season + '/understat/Alex_Telles_1828.csv'),
                    pd.read_csv(PATH + season + '/understat/Emiliano_Buendía_2203.csv'),
                    pd.read_csv(PATH + season + '/understat/Jonny_2280.csv'),
                    pd.read_csv(PATH + season + '/understat/Cristiano_Ronaldo_2371.csv'),
                    pd.read_csv(PATH + season + '/understat/João_Cancelo_2379.csv'),
                #    pd.read_csv(PATH + season + '/understat/André_Gomes_2383.csv'),
                    pd.read_csv(PATH + season + '/understat/Thiago_Silva_3288.csv'),
                    pd.read_csv(PATH + season + '/understat/Lucas_Moura_3293.csv'),
                #    pd.read_csv(PATH + season + '/understat/Ricardo_Pereira_3303.csv'),
                    pd.read_csv(PATH + season + '/understat/Fabinho_3420.csv'),
                    pd.read_csv(PATH + season + '/understat/João_Moutinho_3422.csv'),
                    pd.read_csv(PATH + season + '/understat/Bernardo_Silva_3635.csv'),
                    pd.read_csv(PATH + season + '/understat/Gabriel_Jesus_5543.csv'),
                #    pd.read_csv(PATH + season + '/understat/Anwar_El_Ghazi_5612.csv'),
                    pd.read_csv(PATH + season + '/understat/Richarlison_6026.csv'),
                    pd.read_csv(PATH + season + '/understat/Ederson_6054.csv'),
                    pd.read_csv(PATH + season + '/understat/Douglas_Luiz_6122.csv'),
                    pd.read_csv(PATH + season + '/understat/Nélson_Semedo_6163.csv'),
                    pd.read_csv(PATH + season + '/understat/Pedro_Neto_6382.csv'),
                #    pd.read_csv(PATH + season + '/understat/Júnior_Firpo_6485.csv'),
                    pd.read_csv(PATH + season + '/understat/Rayan_Ait_Nouri_6674.csv'),
                    pd.read_csv(PATH + season + '/understat/Fred_6817.csv'),
                    pd.read_csv(PATH + season + '/understat/Rúben_Neves_6853.csv'),
                    pd.read_csv(PATH + season + '/understat/Emile_Smith-Rowe_7230.csv'),
                    pd.read_csv(PATH + season + '/understat/Diogo_Dalot_7281.csv'),
                    pd.read_csv(PATH + season + '/understat/Ezri_Konsa_Ngoyo_7726.csv'),
                    pd.read_csv(PATH + season + '/understat/Gabriel_Martinelli_7752.csv'),
                    pd.read_csv(PATH + season + '/understat/Daniel_Podence_8291.csv'),
                    pd.read_csv(PATH + season + '/understat/Bruno_Guimarães_8327.csv'),
                    pd.read_csv(PATH + season + '/understat/Alexis_Mac_Allister_8379.csv'),
                    pd.read_csv(PATH + season + '/understat/Rúben_Dias_8961.csv'),
                    pd.read_csv(PATH + season + '/understat/David_Raya_9676.csv'),
                    pd.read_csv(PATH + season + '/understat/Mads_Bech_Sørensen_9683.csv'),
                    pd.read_csv(PATH + season + '/understat/Mads_Roerslev_9685.csv'),
                    pd.read_csv(PATH + season + '/understat/Albert_Sambi_Lokonga_9689.csv'),
                #     pd.read_csv(PATH + season + '/understat/Nuno_Tavares_9691.csv'),
                    pd.read_csv(PATH + season + '/understat/José_Sá_9740.csv')

    ]

    main_dfs_2022 = [
                pd.read_csv(PATH + season + '/players/Joelinton Cássio_Apolinário de Lira_371/gw.csv'),
                pd.read_csv(PATH + season + '/players/Thiago_Alcántara do Nascimento_277/gw.csv'),
                pd.read_csv(PATH + season + '/players/Kevin_De Bruyne_301/gw.csv'),
                pd.read_csv(PATH + season + '/players/Philippe_Coutinho Correia_29/gw.csv'),
        #      pd.read_csv(PATH + season + '/players/Mohamed_Elneny_4/gw.csv'),
                pd.read_csv(PATH + season + '/players/David_De Gea Quintana_327/gw.csv'),
                pd.read_csv(PATH + season + '/players/Virgil_van Dijk_280/gw.csv'),
                pd.read_csv(PATH + season + '/players/Oriol_Romeu Vidal_402/gw.csv'),
                pd.read_csv(PATH + season + '/players/Bruno_Borges Fernandes_333/gw.csv'),
                pd.read_csv(PATH + season + '/players/Emerson_Leite de Souza Junior_445/gw.csv'),
                pd.read_csv(PATH + season + '/players/Alisson_Ramses Becker_281/gw.csv'),
        #     pd.read_csv(PATH + season + '/players/Allan_Marques Loureiro_183/gw.csv'),
                pd.read_csv(PATH + season + '/players/Jorge Luiz_Frello Filho_130/gw.csv'),
            #    pd.read_csv(PATH + season + '/players/Alex_Telles_334/gw.csv'),
                pd.read_csv(PATH + season + '/players/Emiliano_Buendía Stati_42/gw.csv'),
                pd.read_csv(PATH + season + '/players/Jonathan_Castro Otto_477/gw.csv'),
                pd.read_csv(PATH + season + '/players/Cristiano Ronaldo_dos Santos Aveiro_326/gw.csv'),
                pd.read_csv(PATH + season + '/players/João_Cancelo_306/gw.csv'),
            #    pd.read_csv(PATH + season + '/players/André_Tavares Gomes_184/gw.csv'),
                pd.read_csv(PATH + season + '/players/Thiago_Emiliano da Silva_128/gw.csv'),
                pd.read_csv(PATH + season + '/players/Lucas_Rodrigues Moura da Silva_431/gw.csv'),
            #   pd.read_csv(PATH + season + '/players/Ricardo Domingos_Barbosa Pereira_256/gw.csv'),
                pd.read_csv(PATH + season + '/players/Fabio Henrique_Tavares_282/gw.csv'),
                pd.read_csv(PATH + season + '/players/João Filipe Iria_Santos Moutinho_503/gw.csv'),
                pd.read_csv(PATH + season + '/players/Bernardo_Veiga de Carvalho e Silva_311/gw.csv'),
                pd.read_csv(PATH + season + '/players/Gabriel_Fernando de Jesus_28/gw.csv'),
            #  pd.read_csv(PATH + season + '/players/Anwar_El Ghazi_51/gw.csv'),
                pd.read_csv(PATH + season + '/players/Richarlison_de Andrade_454/gw.csv'),
                pd.read_csv(PATH + season + '/players/Ederson_Santana de Moraes_307/gw.csv'),
                pd.read_csv(PATH + season + '/players/Douglas Luiz_Soares de Paulo_46/gw.csv'),
                pd.read_csv(PATH + season + '/players/Nélson_Cabral Semedo_482/gw.csv'),
                pd.read_csv(PATH + season + '/players/Pedro_Lomba Neto_486/gw.csv'),
            #    pd.read_csv(PATH + season + '/players/Héctor Junior_Firpo Adames_239/gw.csv'),
                pd.read_csv(PATH + season + '/players/Rayan_Aït-Nouri_487/gw.csv'),
                pd.read_csv(PATH + season + '/players/Frederico_Rodrigues de Paula Santos_331/gw.csv'),
                pd.read_csv(PATH + season + '/players/Rúben_da Silva Neves_480/gw.csv'),
                pd.read_csv(PATH + season + '/players/Emile_Smith Rowe_12/gw.csv'),
                pd.read_csv(PATH + season + '/players/Diogo_Dalot Teixeira_342/gw.csv'),
                pd.read_csv(PATH + season + '/players/Ezri_Konsa Ngoyo_44/gw.csv'),
                pd.read_csv(PATH + season + '/players/Gabriel_Martinelli Silva_19/gw.csv'),
                pd.read_csv(PATH + season + '/players/Daniel_Castelo Podence_483/gw.csv'),
                pd.read_csv(PATH + season + '/players/Bruno_Guimarães Rodriguez Moura_374/gw.csv'),
                pd.read_csv(PATH + season + '/players/Alexis_Mac Allister_116/gw.csv'),
                pd.read_csv(PATH + season + '/players/Rúben_Gato Alves Dias_312/gw.csv'),
                pd.read_csv(PATH + season + '/players/David_Raya Martin_81/gw.csv'),
                pd.read_csv(PATH + season + '/players/Mads_Bech Sørensen_91/gw.csv'),
                pd.read_csv(PATH + season + '/players/Mads_Roerslev Rasmussen_90/gw.csv'),
                pd.read_csv(PATH + season + '/players/Albert_Sambi Lokonga_18/gw.csv'),
            #    pd.read_csv(PATH + season + '/players/Nuno_Varela Tavares_17/gw.csv'),
                pd.read_csv(PATH + season + '/players/José_Malheiro de Sá_478/gw.csv')
    ]


    understat_dfs_2019 = understat_dfs_2019 + understat_dfs_promoted_players_2019
    main_dfs_2019 = main_dfs_2019 + main_dfs_promoted_players_2019

    season = '2019-20'
    player_info_dict_2019 = {}
    to_be_added_2019 = []
    i=0

    for row in tqdm(range(id_dict_df.shape[0])):
        fpl_id = ids[season]
        understat_str = convert(str(id_dict_df.iloc[row]['Understat_Name'])) + '_' + str(id_dict_df.iloc[row]['Understat_ID']) + '.csv'
        fpl_str = convert(str(id_dict_df.iloc[row]['FPL_Name'])) + '_' + str(id_dict_df.iloc[row][fpl_id])

        try:
            understat_df = pd.read_csv(PATH + '2021-22/understat/' + understat_str)
            main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            player_info_dict_2019[i] = (main_df, understat_df)
            i=i+1
        except:
            to_be_added_2019.append(row)
            continue

    for x in range(len(understat_dfs_2019)):
        understat_df = understat_dfs_2019[x]
        main_df = main_dfs_2019[x]
        player_info_dict_2019[i] = (main_df, understat_df)
        i=i+1
    print('Players from 2019-20 season: ', len(player_info_dict_2019))

    understat_dfs_2020 = understat_dfs_2020 + understat_dfs_promoted_players_2020
    main_dfs_2020 = main_dfs_2020 + main_dfs_promoted_players_2020

    season = '2020-21'
    player_info_dict_2020 = {}
    to_be_added_2020 = []
    i=0

    for row in tqdm(range(id_dict_df.shape[0])):
        fpl_id = ids[season]
        understat_str = convert(str(id_dict_df.iloc[row]['Understat_Name'])) + '_' + str(id_dict_df.iloc[row]['Understat_ID']) + '.csv'
        fpl_str = convert(str(id_dict_df.iloc[row]['FPL_Name'])) + '_' + str(id_dict_df.iloc[row][fpl_id])

        try:
            understat_df = pd.read_csv(PATH + '2021-22/understat/' + understat_str)
            main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            player_info_dict_2020[i] = (main_df, understat_df)
            i=i+1
        except:
            to_be_added_2020.append(row)
            continue

    for x in range(len(understat_dfs_2020)):
        understat_df = understat_dfs_2020[x]
        main_df = main_dfs_2020[x]
        player_info_dict_2020[i] = (main_df, understat_df)
        i=i+1

    print('Players from 2020-21 season: ', len(player_info_dict_2020))

    season = '2021-22'
    player_info_dict_2021 = {}
    to_be_added_2021 = []
    i=0

    for row in tqdm(range(id_dict_df.shape[0])):
        fpl_id = ids[season]
        understat_str = convert(str(id_dict_df.iloc[row]['Understat_Name'])) + '_' + str(id_dict_df.iloc[row]['Understat_ID']) + '.csv'
        fpl_str = convert(str(id_dict_df.iloc[row]['FPL_Name'])) + '_' + str(id_dict_df.iloc[row][fpl_id])

        try:
            understat_df = pd.read_csv(PATH + '2021-22/understat/' + understat_str)
            main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            player_info_dict_2021[i] = (main_df, understat_df)
            i=i+1
        except:
            to_be_added_2021.append(row)
            continue
    
    for x in range(len(understat_dfs_2021)):
        understat_df = understat_dfs_2021[x]
        main_df = main_dfs_2021[x]
        player_info_dict_2021[i] = (main_df, understat_df)
        i=i+1
    
    print('Players from 2021-22 season: ', len(player_info_dict_2021))

    season = '2022-23'
    player_info_dict_2022 = {}
    to_be_added_2022 = []
    i=0

    for row in tqdm(range(1,id_dict_df.shape[0])):
        fpl_id = ids[season]
        understat_str = convert(str(id_dict_df.iloc[row]['Understat_Name'])) + '_' + str(id_dict_df.iloc[row]['Understat_ID']) + '.csv'
        fpl_str = convert(str(id_dict_df.iloc[row]['FPL_Name'])) + '_' + str(id_dict_df.iloc[row][fpl_id])

        try:
            understat_df = pd.read_csv(PATH + season + '/understat/' + understat_str)
            main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            player_info_dict_2022[i] = (main_df, understat_df)
            i=i+1
        except: 
            to_be_added_2022.append(row)
            continue
    
    for x in range(len(understat_dfs_2022)):
        understat_df = understat_dfs_2022[x]
        main_df = main_dfs_2022[x]
        player_info_dict_2022[i] = (main_df, understat_df)
        i=i+1
    print('Players from 2022-23 season: ', len(player_info_dict_2022))

    player_info_dict = {
        '2019-20': player_info_dict_2019,
        '2020-21': player_info_dict_2020,
        '2021-22': player_info_dict_2021,
        '2022-23': player_info_dict_2022
    }

    return player_info_dict


'''
from tqdm import tqdm
import asyncio
import json
import pickle
import pandas as pd
import aiohttp
from understat import Understat
import nest_asyncio
nest_asyncio.apply()


async def player_understat_file(id):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        player_matches = await understat.get_player_matches(id)
        player_matches = pd.DataFrame(player_matches)
        return player_matches

player_info_dict = {
    '2016-17': {},
    '2017-18': {},
    '2018-19': {},
    '2019-20': {},
    '2020-21': {},
    '2021-22': {},
    '2022-23': {}
}

def players_data(id_dict_df, seasons, ids, PATH):
    for season in seasons:
        print('Season: ' + season)
        i = 0
        fpl_id = ids[season]
        df = id_dict_df[(id_dict_df[fpl_id] > 0) & (id_dict_df['understat'] > 0)]

        for row in tqdm(range(df.shape[0])):
            if season != '2016-17' and season != '2017-18':
                fpl_str = df.iloc[row]['first_name'] + '_' + df.iloc[row]['second_name'] + '_' + str(df.iloc[row][fpl_id])
            else:
                fpl_str = df.iloc[row]['first_name'] + '_' + df.iloc[row]['second_name']
            try:
                loop = asyncio.get_event_loop()
                understat_df = loop.run_until_complete(player_understat_file(df.iloc[row]['understat']))
                main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
                player_info_dict[season][i] = (main_df, understat_df)
                i=i+1
            except:
                continue
        print(str(len(player_info_dict[season])) + ' players added.')
    
    with open('../created_datasets/player_info_dict.pkl', 'wb') as f:
        pickle.dump(player_info_dict, f)
    return player_info_dict
'''